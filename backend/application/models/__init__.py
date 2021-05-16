"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: __init__.py.py
@time: 2020/12/26 13:46
@desc: ORM存放，计划是放置关系型数据库的模型，或许也可以放置图数据的？
"""

from application.models.herb.herb import Herb
from application.models.prescription.prescription import Prescription
from application.models.disease import Disease
from application.models.ingredient import Ingredient
from application.models.symptom import MMSymptom, TCMSymptom
from application.models.target import Target
from application.models.dict_table import DicTableData, DicTableType
from application.models.related_tables import *
from application.models.authbase.user import User
from application.models.authbase.role import Role
from application.models.authbase.logs import AnalysesLog
from application.models.labels import Labels

basic_data_models = [
    "Herb",
    "Prescription",
    "Disease",
    "Ingredient",
    "MMSymptom",
    "TCMSymptom",
    "Target",
]

# basic_data_models_str = [
#     Herb,
#     Prescription,
#     Disease,
#     Ingredient,
#     MMSymptom,
#     TCMSymptom,
#     Target,
# ]
