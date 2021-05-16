# -*- coding: utf-8 -*-
"""
    :time: 2021/2/23 16:24
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: target.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from wtforms import Form, StringField


class TargetForm(Form):
    id = StringField("id", default="")
    s_gene_symbol = StringField("基因符号", default="")
    s_chromosome = StringField("染色体", default="")
    s_name = StringField("名称", default="")
    s_protein_name = StringField("蛋白质", default="")
