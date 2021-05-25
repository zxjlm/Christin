"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: data_manage_api_v2.py
@time: 2021/5/24 6:27 下午
@desc:
"""
from flask import Blueprint, jsonify, request

from application.controllers.dashboard_datamanage import get_model_columns, get_model_paginated_data

dm_v2_bp = Blueprint("data_manage_api_v2", __name__, url_prefix="/dashboard/api/v2")


@dm_v2_bp.get('/get_columns/<model>')
def get_columns(model):
    return jsonify(get_model_columns(model))


@dm_v2_bp.post('/get_table_data')
def get_table_data():
    return jsonify(get_model_paginated_data(**request.json))
