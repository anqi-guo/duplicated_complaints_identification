import regex as re
import jieba
import json
import hanlp
from tqdm.auto import tqdm
import pandas as pd
from powersmart.utils import file_util
tqdm.pandas()

tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
ner = hanlp.load(hanlp.pretrained.ner.MSRA_NER_ELECTRA_SMALL_ZH)
conf = file_util.get_config()


def read_query(query):
    engine = file_util.get_engine()
    df = pd.read_sql_query(query, engine, index_col=None)
    return df


def extract_problem(text):
    '''
    从文本中提取关键语句

    :param text: 文本
    :return: 关键语句
    '''
    # 删掉标点符号
    text = re.sub(r'\p{P}+', '', text)
    # 删掉空格、换行符、信息保密、信息不保密、距离、时间、数字、投诉人信息
    text = re.sub(r'(\s|\n|信息[不]?保密|\d+[m米年月日]?|(.{1}先生|.{1}女士|市民)(来电)?反映)', '', text)

    if '问题描述' in text and '诉求目的' in text:
        text = re.search(r'(?<=问题描述).*(?=诉求目的)', text).group()

    # 删掉停用词
    stopwords_file = file_util.get_file(conf['stopwords'])
    with open(stopwords_file) as f:
        stopwords = f.read().splitlines()

    seg_list = jieba.cut(text)
    result = ''.join([s for s in seg_list if s not in stopwords])

    return result


def extract_location(text):
    '''
    从文本中提取命名实体为LOCATION或者ORGANIZATION的词
    :param text: 文本
    :return: 词
    '''
    # 分词
    tokenized_text = tok(text)
    # 先把省市区删掉
    clean_tokenized_text = [t for t in tokenized_text if not t.endswith(('省','市','县','镇','区'))]
    # 提取命名实体
    nerred_text = ner(clean_tokenized_text)
    # 提取命名实体是ORGANIZATION或者LOCATION，且结尾不是市镇区县的词
    locations = [l[0] for l in nerred_text if (l[1] == 'ORGANIZATION' or l[1] == 'LOCATION')]
    # 把路具体多少号删掉
    clean_locations = [re.sub('\d+[号]?','',l) for l in locations]

    return list(set(clean_locations))


def extract_apartments(text):
    '''
    从文本中提取小区名称和地址
    :param text: 文本
    :return: 小区名称和地址
    '''
    address_list = []

    apartments_file = file_util.get_file(conf['apartments'])
    with open(apartments_file) as json_file:
        apartments = json.load(json_file)

    for apt, addr in apartments.items():
        if apt in text:
            address_list.append(apt)
            address_list.extend(addr)

    return address_list


def extract_address(text):
    '''
    从文本中提取所有和地址有关的信息
    :param text: 文本
    :return: 地址信息
    '''
    location_list = extract_location(text)
    apartments_list = extract_apartments(text)

    address_list = location_list + apartments_list
    address_list = [l for l in address_list if len(l) > 2]

    address_list_sorted = sorted(list(set(address_list)), key=len)
    address_str = ','.join(address_list_sorted)
    address_list_ch = re.findall('[\u4e00-\u9fa5]', address_str)

    return ','.join(address_list_ch)