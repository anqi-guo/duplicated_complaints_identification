import yaml
import os
from sqlalchemy import create_engine
import regex as re


def get_file(file_name, relative_path='resources'):
    current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = re.sub('powersmart.*',f'{relative_path}/{file_name}',current_path)
    return file_path


def get_config():
    file = get_file('config.yaml')
    with open(file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    return data


def get_query(file):
    with open(file, 'r', encoding='utf-8') as f:
        query = f.read()

    return query


def get_engine():
    db = get_config()['db_info']
    engine = create_engine(
        f'mssql+pymssql://{db["username"]}:{db["password"]}@{db["host"]}:{db["port"]}/{db["database"]}')
    return engine


def save_data(data, table):
    db = get_config()['db_info']
    engine = get_engine()
    data.to_sql(name=table,
                con=engine,
                schema='dbo',
                if_exists='append',
                chunksize=1000,
                index=False)