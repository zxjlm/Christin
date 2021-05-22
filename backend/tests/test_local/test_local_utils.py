"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: test_local_utils.py
@time: 2021/5/22 8:36 下午
@desc:
"""
from application.utils.docker_handler import get_all_container_and_classify


def test_get_all_container_and_classify():
    assert list(get_all_container_and_classify().keys()) == ['running', 'exited']
