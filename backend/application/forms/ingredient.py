# -*- coding: utf-8 -*-
"""
    :time: 2021/2/23 16:16
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: ingredient.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""

from wtforms import Form, StringField, FloatField


class IngredientForm(Form):
    id = StringField("id", default="")
    s_name = StringField("名称", default="")
    s_molecule_formula = StringField("分子式", default="")
    f_molecule_weight = FloatField("分子权重", default="")
    f_ob_score = FloatField("口服生物利用度评分", default="")
    s_alias = StringField("别名", default="")
