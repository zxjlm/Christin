# -*- coding: utf-8 -*-
"""
    :time: 2021/2/23 16:14
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: disease.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from wtforms import Form, StringField


class DiseaseForm(Form):
    id = StringField("id", default="")
    s_name = StringField("名称", default="")
    s_disease_definition = StringField("定义", default="")
