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


def needed_item(title, value):
    return {"title": title,
            "dataIndex": "title",
            "formItemProps":
                {"rules": [{"required": True, "message": "此项为必填项"}]},
            "width": "m",
            "initialValue": value}
