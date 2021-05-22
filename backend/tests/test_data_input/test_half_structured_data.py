"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: test_half_structured_data.py
@time: 2021/1/16 23:14
@desc:
"""
from werkzeug.datastructures import FileStorage

from config.settings import ROOT_PATH


def test_half_structure_data(client):
    """
    测试 - 半结构化数据录入
    Args:
        client:

    Returns:

    """

    my_file = FileStorage(
        stream=open(ROOT_PATH + '/datas/structural_data_json.json', "rb"),
        filename='structural_data_json.json',
        content_type="application/json",
    ),

    response = client.post('/main/api/v2/extract_from_json', data={'files': my_file})

    assert response.status_code == 200 and len(response.json['data']) == 5 and response.json['code'] == '200'
