"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: request_warpper.py
@time: 2021/5/19 3:04 下午
@desc:
"""
import time
from functools import wraps

from flask import jsonify
from loguru import logger


def normal_api_wrapper(func):
    """
    api装饰器, 外装请求的状态码/请求花费的时间等内容
    Args:
        func:

    Returns:

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            spend = time.time() - start
            return jsonify({**result, 'spend_time': spend, 'code': 200})
        except Exception as _e:
            logger.exception(_e)
            return jsonify({'code': 400, 'msg': str(_e), 'err_func': func.__name__}), 400

    return wrapper
