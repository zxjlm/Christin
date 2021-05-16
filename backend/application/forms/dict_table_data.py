# -*- coding: utf-8 -*-
"""
    :time: 2021/2/20 15:54
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: dict_table_data.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from wtforms import Form, StringField, SelectField

from application.controllers.dict_data_table import get_dic_types


class DicTableDataForm(Form):
    """"""

    id = StringField("id", default="")
    s_name = StringField("名称", default="")
    s_en_name = StringField("英文名称", default="")
    type_name = SelectField("类型名称", choices=get_dic_types(), default="")
    s_remark = StringField("备注", default="")
