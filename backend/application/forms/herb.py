# -*- coding: utf-8 -*-
"""
    :time: 2021/2/3 17:00
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: herb.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from wtforms import Form, StringField, SelectMultipleField, SelectField

from application.controllers.dict_data_table import (
    get_four_nature,
    get_meridians,
    get_five_tastes,
    get_floating_and_sinking,
    get_herb_subclass,
    get_herb_broad_heading,
)


class HerbForm(Form):
    id = StringField("id", default="")
    s_name = StringField("名称", default="")
    s_en_name = StringField("s_en_name", default="")
    s_latin_name = StringField("s_latin_name", default="")
    s_abbreviated_name = StringField("s_abbreviated_name", default="")
    s_usage = StringField("s_usage", default="")
    s_herb_affiliate = StringField("s_herb_affiliate", default="")
    s_origin = StringField("s_origin", default="")
    s_application = StringField("s_application", default="")
    s_foundation = StringField("s_foundation", default="")
    s_prison = StringField("s_prison", default="")
    s_ancient_literature = StringField("s_ancient_literature", default="")
    s_chemical = StringField("s_chemical", default="")
    s_discussion = StringField("s_discussion", default="")
    s_affiliate = StringField("s_affiliate", default="")
    s_pharmacological_action = StringField("s_pharmacological_action", default="")
    s_untoward_effect = StringField("s_untoward_effect", default="")
    s_normal_remark = StringField("s_normal_remark", default="")
    json_remark = StringField("json_remark", default="")

    # four_natures = StringField('four_natures', default='')
    four_natures = SelectMultipleField(
        "four_natures", choices=get_four_nature(), default=[]
    )
    five_tastes = SelectMultipleField(
        "five_tastes", choices=get_five_tastes(), default=[]
    )
    floating_and_sinking = SelectMultipleField(
        "floating_and_sinking", choices=get_floating_and_sinking(), default=[]
    )
    meridians = SelectMultipleField("meridians", choices=get_meridians(), default=[])
    herb_broad_heading = SelectField(
        "herb_broad_heading", choices=get_herb_broad_heading(), default=""
    )
    herb_subclass = SelectField(
        "herb_subclass", choices=get_herb_subclass(), default=""
    )
