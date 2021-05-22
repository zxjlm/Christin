"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: function_status_wrapper.py
@time: 2021/5/22 7:35 下午
@desc:
"""
import warnings
from functools import wraps


def function_departed_warning(new_func: str = None, description: str = None):
    """
    弃用函数的说明
    Args:
        new_func: 新函数名
        description: 废弃原因

    Returns:

    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            messages = [f"{func.__name__} will be deprecated"]
            new_func and messages.append(f'use f{new_func} instead')
            description and messages.append(f'reason is {description}')
            warnings.warn(
                ', '.join(messages),
                DeprecationWarning,
                2
            )
            return result

        return wrapper

    return decorate
