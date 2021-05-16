# -*- coding: utf-8 -*-
"""
    :time: 2021/2/24 16:38
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: custom_exceptions.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""


class UnknownValueException(Exception):
    """
    不明数据

    可能是攻击
    """

    ...


class Neo4jUpdateFailedException(Exception):
    """
    在同步更新时,neo4j更新失败.
    出于数据一致性的考虑，回滚本次更新
    """

    ...
