# -*- coding: utf-8 -*-
"""
    :time: 2021/2/4 9:47
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: prescription.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from wtforms import Form, StringField, TextAreaField


class PrescriptionForm(Form):
    id = StringField("id", default="")

    s_name = StringField("名字", default="")
    s_abbreviated_name = StringField("首字母缩写", default="")
    s_dosage_form = StringField("剂型", default="")
    s_indications = StringField("主治", default="")
    s_origin = StringField("出处", default="")
    s_modified = StringField("加减", default="")
    s_complain = StringField("方解", default="")
    s_function = StringField("功用", default="")
    s_compatibility = StringField("宜忌", default="")
    s_bad_effect = StringField("不良反应", default="")
    s_prison = StringField("毒性实验", default="")
    s_chemical_component = StringField("化学成分", default="")
    s_physicochemical_property = StringField("理化性质", default="")

    s_clinic = TextAreaField("临床应用", default="")
    s_pharmacological_action = TextAreaField("药理作用", default="")
    s_usage = TextAreaField("用法", default="")
    s_discussion = TextAreaField("各家论述", default="")
    s_warning = TextAreaField("用药禁忌", default="")
    s_manufacturer = TextAreaField("生产厂家", default="")
    s_normal_remark = TextAreaField("普通备注", default="")
    json_remark = TextAreaField("Json备注", default="")
