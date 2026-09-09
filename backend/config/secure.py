"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: secure.py
@time: 2020/8/10 21:54
@desc:
"""
from config.settings import (
    MAIL_PWD,
    MAIL_USER,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_PWD,
    MYSQL_USER,
    NEO_HOST,
    NEO_PORT,
    NEO_PWD,
)


class SecureInfo:
    """
    python-Levenshtein==0.12.0
    """

    @staticmethod
    def get_mysql_of_development():
        return f"mysql+cymysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/christin"

    @staticmethod
    def get_mysql_of_production():
        # if os.sys.platform not in ['linux', 'darwin']:
        #     return 'mysql+cymysql://root:NKKMCDWJFW3CFRwJcA@39.108.229.166' \
        #            ':6622/christin'
        # else:
        return f"mysql+cymysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/christin"

    @staticmethod
    def get_mysql_of_test():
        return "sqlite:///:memory:"

    @staticmethod
    def get_mail_passwd():
        return MAIL_PWD

    @staticmethod
    def get_mail_user():
        return MAIL_USER

    @staticmethod
    def get_neo4j_config():
        return {
            "profile": f"bolt://{NEO_HOST}:{NEO_PORT}",
            "name": "neo4j",
            "password": NEO_PWD,
        }

    @staticmethod
    def get_neo4j_blot():
        return f"bolt://{NEO_HOST}:{NEO_PORT}"

    @staticmethod
    def get_neo4j_password():
        return NEO_PWD

    @staticmethod
    def get_neo4j_port():
        return NEO_PORT
