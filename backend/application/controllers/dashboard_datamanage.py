# -*- coding: utf-8 -*-
"""
    :time: 2021/2/20 16:10
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: dashboard_datamanage.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import importlib

from application.controllers.common_model_opt import data_query_particular, query_data_from_models


def query_data_controller(data):
    """
    基础数据的查询
    Args:
        data:

    Returns: 可填充的基础数据的表单

    """
    msg = data_query_particular(data["data"], data["type"])
    if msg:
        tmp_cls = importlib.import_module("application.forms", data["type"] + "Form")
        form = getattr(tmp_cls, data["type"] + "Form")()
        for k, v in msg.items():
            setattr(getattr(form, k), "data", v)
        return form
    else:
        return False


def create_data_controller(data):
    """
    创建基础数据
    Args:
        data:

    Returns: 创建基础数据所用的数据表单

    """
    tmp_cls = importlib.import_module("application.forms", data["type"] + "Form")

    form = getattr(tmp_cls, data["type"] + "Form")()
    delattr(form, "id")
    return form


def switch_type_title(type_: str) -> str:
    """
    输出该类型所对应的标题组
    Args:
        type_:

    Returns:

    """
    ret = {
        "Herb": "中药",
        "Prescription": "处方",
        "Disease": "疾病",
        "Ingredient": "中药组成",
        "MMSymptom": "症状(MM)",
        "TCMSymptom": "症状(TCM)",
        "Target": "基因",
        "DicTableData": "字典表",
        "LoginData": "登录记录",
        "User": "用户数据",
        "Role": "角色数据",
    }
    return ret.get(type_, "")


def check_page_style(type_: str) -> int:
    """
    检查页面的样式风格
    Args:
        type_:

    Returns:

    """
    dic = {1: ["User", "LoginData"]}  # 不可手动添加
    for k, v in dic.items():
        if type_ in v:
            return k
    return 0


def get_data_table_fields(type_):
    """
    获取数据表需要展示的字段
    Args:
        type_:

    Returns:

    """
    mod = importlib.import_module("application.models", type_)
    return getattr(mod, type_).data_table_fields()


def get_model_columns(model):
    mod = importlib.import_module("application.models", model)
    tmp = getattr(mod, model)
    # page_res = query_data_from_models(tmp, 1, 20)
    # result = {'initData': [item.to_dict() for item in page_res.items], 'columns': getattr(mod, model).normal_columns()}
    # return result
    return getattr(mod, model).normal_columns()


def get_model_paginated_data(model, current, **kwargs):
    condition = {}
    mod = importlib.import_module("application.models", model)
    tmp = getattr(mod, model)
    if 's_name' in kwargs.keys():
        condition = {'s_name': kwargs.pop('s_name')}
    page_res = query_data_from_models(tmp, current, kwargs.pop('pageSize'), condition=condition)
    result = [item.to_dict() for item in page_res.items]
    return {'data': result, 'success': True, 'total': page_res.total}
