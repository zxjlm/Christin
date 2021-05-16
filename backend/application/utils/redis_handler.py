# -*- coding: utf-8 -*-
"""
    :time: 2021/2/1 16:02
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: redis_handler.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""


def get_all_data_from_redis_list(r, key):
    """
    安全获取list结构中的所有数据
    Args:
        r: redis对象
        key:

    Returns:

    """
    res = []
    pop_data = r.rpop(key)
    while pop_data:
        res.append(pop_data)
        pop_data = r.rpop(key)
    return [foo.decode("utf-8") for foo in res]
