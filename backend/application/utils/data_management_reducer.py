# -*- coding: utf-8 -*-
"""
    :time: 2021/1/27 17:33
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: data_management_reducer.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from config.settings import LOCK_MODELS


def get_cls_primary_key(cls_str: str):
    """
    获取表的主键
    Returns:

    """
    dic = {
        "Herb": "bin_hid",
        "Prescription": "bin_pid",
        "Disease": "bin_id",
        "Ingredient": "bin_id",
        "TCMSymptom": "bin_id",
        "MMSymptom": "bin_id",
        "Target": "bin_id",
    }
    return dic.get(cls_str, "id")


def is_locked_field_in(data: dict, cls):
    """
    是否包含锁定字段
    Args:
        data:
        cls:

    Returns:

    """
    for field in cls.lock_field():
        if field in data:
            return True
    return False


def check_model_name(type_):
    """
    检校model名是否存在
    Args:
        type_:

    Returns:

    """

    if type_ in LOCK_MODELS:
        return True
    else:
        return False
