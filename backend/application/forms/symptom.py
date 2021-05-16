# -*- coding: utf-8 -*-
"""
    :time: 2021/2/23 16:20
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: symptom.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from wtforms import Form, StringField


class MMSymptomForm(Form):
    id = StringField("id", default="")
    s_name = StringField("名称", default="")
    s_mm_symptom_definition = StringField("定义", default="")
    s_mm_tree_numbers = StringField("MeSH标号", default="")


class TCMSymptomFrom(Form):
    id = StringField("id", default="")
    s_name = StringField("名称", default="")
    s_pinyin_name = StringField("拼音", default="")
    s_symptom_definition = StringField("定义", default="")
    s_symptom_locus = StringField("locus", default="")
    s_symptom_property = StringField("属性", default="")
