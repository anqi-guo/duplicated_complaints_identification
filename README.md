# 重复投诉线索识别
这个repository包含了对原始数据的清洗，标注，建模，和推断。具体步骤如下
1. [从网站爬取新旧楼盘/小区的名称和地址](https://github.com/anqi-guo/duplicated_complaints_identification/blob/main/1_webscrape_loupan.ipynb)
2. [清洗原始数据，提取地址信息，将相同行政区划且地址有重叠的文本配对，保存](https://github.com/anqi-guo/duplicated_complaints_identification/blob/main/2_preprocess_unlabeled_data.ipynb)
3. 人工标注
4. [用SentenceBERT预训练语言模型对标注数据进行微调，保存模型](https://github.com/anqi-guo/duplicated_complaints_identification/blob/main/4_sbert.ipynb)
5. [对于模型分错的样本，进行数据扩充，然后再次训练模型（回到第4步）](https://github.com/anqi-guo/duplicated_complaints_identification/blob/main/3_process_labeled_data.ipynb)
6. [用模型从所有未标注的原始数据进行推断](https://github.com/anqi-guo/duplicated_complaints_identification/blob/main/5_infer.ipynb)
