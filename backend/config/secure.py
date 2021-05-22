"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: secure.py
@time: 2020/8/10 21:54
@desc:
"""
from config.settings import MYSQL_HOST, MYSQL_PWD, MYSQL_PORT, MYSQL_USER


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
        return "WEYBIIWFZOJCKWOA"

    @staticmethod
    def get_mail_user():
        return "zxjlm233@163.com"

    @staticmethod
    def get_neo4j_config():
        return {
            "profile": "bolt://39.99.178.69:7687",
            "name": "neo4j",
            "password": "zxjzxj233",
        }

    @staticmethod
    def get_neo4j_blot():
        # return 'bolt://39.99.178.69:7687'
        return "bolt://localhost:7687"

    @staticmethod
    def get_neo4j_password():
        return "zxjzxj233"

    @staticmethod
    def get_neo4j_port():
        return "7687"
