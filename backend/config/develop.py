# -*- coding:utf-8 -*-
__author__ = "harumonia"

from config.baseconfig import ConfigBase


class DevelopmentConfig(ConfigBase):
    DEBUG = True
    MODE = "development"
    WTF_CSRF_ENABLED = False
