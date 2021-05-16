# -*- coding: utf-8 -*-
"""
    :time: 2021/2/8 17:28
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: mysql_handler.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import importlib
import json
import re

import cymysql
from loguru import logger

from application.models import basic_data_models
from config.settings import MYSQL_HOST


def change_project_status(id_, config=None, runtime=None, status=1):
    """
    任务完成时更新数据库
    Args:
        status: 任务的状态 1: 成功  0: 失败
        runtime:
        id_:
        config:

    Returns:

    """
    conn = cymysql.connect(host=MYSQL_HOST, user="root", passwd="root", db="christin")
    cur = conn.cursor()
    try:
        cur.execute(
            f"UPDATE christin.analyses_log SET i_status={status} "
            f"WHERE s_mark='{id_}';"
        )
        if runtime:
            cur.execute(
                f"UPDATE christin.analyses_log SET "
                f"f_runtime={runtime} WHERE s_mark='{id_}';"
            )
        if config:
            j_config = json.dumps(config, ensure_ascii=False)
            cur.execute(
                f"UPDATE christin.analyses_log SET "
                f"j_remark='{j_config}' WHERE s_mark='{id_}';"
            )
        conn.commit()
    except Exception as _e:
        logger.error(_e)
        cur.execute(
            f"UPDATE christin.analyses_log SET i_status=2 WHERE s_mark='{id_}';"
        )
    cur.close()
    conn.close()


def update_task_process(id_, current_step: int):
    conn = cymysql.connect(host=MYSQL_HOST, user="root", passwd="root", db="christin")
    cur = conn.cursor()
    try:
        cur.execute(
            f"UPDATE christin.analyses_log SET i_current_step={current_step} "
            f"WHERE s_mark='{id_}';"
        )
        conn.commit()
    except Exception as _e:
        logger.error(_e)
    cur.close()
    conn.close()


def generate_validate_query() -> (str, set):
    """
    生成查询的sql语句(针对结构化数据录入)
    Returns:

    """
    for model in basic_data_models:
        mod = getattr(importlib.import_module("application.models", model), model)
        tmp = mod()
        fields = set(filter(lambda x: re.match("[sfj]_", x), tmp.__dir__()))
        query = f"SELECT * FROM {mod.__tablename__}"
        yield query, fields, mod.__tablename__


def mysql_query_operator(
    host: str,
    port: str,
    username: str,
    password: str,
    db_name: str,
    query_sql: str,
    numbers: int = -1,
) -> (list, list):
    """
    mysql 查询语句的封装
    Args:
        numbers:
        query_sql:
        host:
        port:
        username:
        password:
        db_name:

    Returns:

    """
    try:
        db = cymysql.connect(
            host=host, port=int(port), user=username, passwd=password, db=db_name
        )
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
    except Exception as _e:
        logger.exception(_e)
        raise Exception("can`t connect to database")
    try:
        # 执行SQL语句
        cursor.execute(query_sql)
        # 获取所有记录列表
        if numbers != -1:
            results = cursor.fetchmany(numbers)
        else:
            results = cursor.fetchall()
        cols = [foo[0] for foo in cursor.description]

    except Exception as _e:
        logger.exception(_e)
        raise Exception("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()

    return results, cols
