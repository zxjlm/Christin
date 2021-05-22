"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: file_handler.py
@time: 2021/5/4 10:47 上午
@desc:
"""
import json

from werkzeug.datastructures import FileStorage
import pandas as pd

from application.models import basic_data_models
from application.utils.function_status_wrapper import function_departed_warning
from application.utils.mysql_handler import generate_validate_query


def check_file_type():
    """
    检查文件类型
    Returns:

    """


def extract_data_from_csv_file(file: FileStorage) -> list:
    """
    从csv文件中提取数据
    Returns:

    """
    df = pd.read_csv(file)
    return list(df["data"])


def extract_data_from_excel_file(file: FileStorage) -> list:
    """
    从excel文件中提取数据
    Returns:

    """
    df = pd.read_excel(file, engine="openpyxl")
    return list(df["data"])


def extract_data_from_text_file(file: FileStorage) -> list:
    """
    从文本文件中提取数据
    Returns:

    """
    return [line.decode().strip() for line in file.stream.readlines()]


def extract_data_from_json_file(file: FileStorage):
    """
    从json文件中提取数据
    Args:
        file:

    Returns:

    """
    file_data = json.loads(file.stream.read())
    if isinstance(file_data, list):
        if len(file_data) > 0 and file_data[0].get("EntType"):
            return file_data
        return "invalid data"
    elif isinstance(file_data, dict):
        return "dict type is valid"
    return "not a json file"


@function_departed_warning()
def parser_json_file_v1(data: dict, result: dict):
    """
    解析json文件,提取出符合规范的数据
    Returns:

    """
    sql_generator = generate_validate_query()
    mapper = dict(zip(basic_data_models, [fields for _, fields, _ in sql_generator]))

    for k, v in data.items():
        if k in basic_data_models and isinstance(v, list):
            result.setdefault(k, [])
            for item in filter(lambda x: isinstance(x, dict), v):
                tmp = {}
                for field in mapper[k]:
                    tmp[field] = item.get(field)
                result[k].append(tmp)
