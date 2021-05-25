"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: generic_form_schema.py
@time: 2021/5/25 10:49 上午
@desc:
"""


def string_item(title, data_index, value, required=False, readonly=False):
    """
    必填项
    Args:
        readonly:
        required:
        title:
        data_index:
        value:

    Returns:

    """
    item_props = {"rules": [{"required": True, "message": "此项为必填项"}]} if required else {}
    return {
        "title": title,
        "dataIndex": data_index,
        "formItemProps": item_props,
        "width": "m",
        "initialValue": value,
        "disable": readonly,
    }


def get_field_comment_mapper(cls):
    """
    获取字段的中英文对照表
    Args:
        cls:

    Returns:

    """
    res = {}
    for foo in cls.__dict__:
        if getattr(getattr(cls, foo), 'expression', None) is not None:
            if getattr(getattr(cls, foo).expression, 'comment', None) is not None:
                res[foo] = getattr(cls, foo).expression.comment
    return res
