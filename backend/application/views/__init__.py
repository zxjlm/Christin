"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: __init__.py.py
@time: 2020/12/26 13:47
@desc:
"""
from application.views.dashboard.dashboard import dash_bp
from application.views.dashboard.data_manage import dm_bp
from application.views.dashboard.data_manage_api_v2 import dm_v2_bp
from application.views.main.main import main_bp
from application.views.main.main_api import main_api_bp
from application.views.main.main_api_v2 import main_api_v2_bp
from application.views.ner_api.ner_api import ner_api_bp

all_bp = [main_bp, dash_bp, dm_bp, main_api_bp, main_api_v2_bp, dm_v2_bp, ner_api_bp]
