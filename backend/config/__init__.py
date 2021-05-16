"""
@author: harumonia
@site:
@datetime: 2020/4/15 22:16
@software: PyCharm
@description: 这里存放基础的配置文件,分为三大类:生产、开发、测试
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


def import_config(mode):
    if mode == "development":
        from config.develop import DevelopmentConfig

        return DevelopmentConfig
    elif mode == "production":
        from config.production import ProductionConfig

        return ProductionConfig
    else:
        from config.test import TestingConfig

        return TestingConfig
    # # 'testing': TestingConfig,
    # # 'default': DevelopmentConfig
