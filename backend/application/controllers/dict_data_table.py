# -*- coding: utf-8 -*-
"""
    :time: 2021/2/24 11:02
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: dict_data_table.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from application.models.dict_table import DicTableData, DicTableType


# 默认字典表是定死不变的，如果字典表发生变动，这里需要手动更改对应的id
def get_herb_broad_heading():
    res = DicTableData.query.filter_by(type_id=1).all()
    return [(str(foo.id), foo.s_name) for foo in res]


def get_herb_subclass():
    res = DicTableData.query.filter_by(type_id=2).all()
    return [(str(foo.id), foo.s_name) for foo in res]


def get_four_nature():
    res = DicTableData.query.filter_by(type_id=5).all()
    return [(str(foo.id), foo.s_name) for foo in res]


def get_five_tastes():
    res = DicTableData.query.filter_by(type_id=6).all()
    return [(str(foo.id), foo.s_name) for foo in res]


def get_meridians():
    res = DicTableData.query.filter_by(type_id=8).all()
    return [(str(foo.id), foo.s_name) for foo in res]


def get_floating_and_sinking():
    res = DicTableData.query.filter_by(type_id=7).all()
    return [(str(foo.id), foo.s_name) for foo in res]


def get_dic_types():
    res = DicTableType.query.all()
    return [(str(foo.id), foo.s_name) for foo in res]
