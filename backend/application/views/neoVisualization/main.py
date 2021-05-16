"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: main.py
@time: 2021/5/12 12:50 下午
@desc:
"""
from flask import Blueprint

neo_bp = Blueprint("main", __name__, static_folder="static/ant-neo")
