# -*- coding:utf-8 -*-

__author__ = "harumonia"

import os

api_level = "v1.0"

mail_title = "XMiner的邮件"

file_discription_dic = {
    "freq": "Analysis of frequent itemsets",
    "rules": "Analysis of association rules",
    "report": "Analysis report of this project",
}

LOCK_MODELS = [
    "Herb",
    "Role",
    "User",
    "DicTableData",
    "DicTableType",
    "Disease",
    "HerbAlias",
    "HerbEffect",
    "Ingredient",
    "MMSymptom",
    "Prescription",
    "Target",
    "TCMSymptom",
]

LANGUAGES = {"en": "English", "zh": "Chinese"}

REDIS_HOST = os.environ.get("CHRISTIN_REDIS_HOST", "localhost")
NEO_HOST = os.environ.get("CHRISTIN_NEO_HOST", "localhost")
MYSQL_HOST = os.environ.get("CHRISTIN_MYSQL_HOST", "localhost")
MYSQL_PORT = os.environ.get("CHRISTIN_MYSQL_PORT", "3306")
MYSQL_USER = os.environ.get("CHRISTIN_MYSQL_USER", "root")
MYSQL_PWD = os.environ.get("CHRISTIN_MYSQL_PWD", "root")
SERVER = NEO_HOST

SWAGGER_FOLDER = os.path.join("..", "..", "swagger_files")

DOCKER_NEO4J_IMAGES_VERSION = [
    "neo4j/neo4j-arm64-experimental:4.2.5-arm64",
    "neo4j:3.5.12",
]

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
