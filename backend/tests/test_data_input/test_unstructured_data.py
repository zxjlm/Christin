"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: test_unstructured_data.py
@time: 2021/1/16 23:14
@desc:
"""
from werkzeug.datastructures import FileStorage

from config.settings import ROOT_PATH


def test_normal_data(client):
    my_file = FileStorage(
        stream=open(ROOT_PATH + '/datas/test_data.txt', "rb"),
        filename="test_data.txt",
        content_type="text/plain",
    ),

    response = client.post('/main/api/v2/extract_from_text', data={'files': my_file})

    assert response.status_code == 200 and len(response.json['data']) == 4
