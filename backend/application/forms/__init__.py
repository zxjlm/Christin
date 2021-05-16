"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: __init__.py.py
@time: 2021/1/24 16:20
@desc:
"""
from .dict_table_data import DicTableDataForm
from .herb import HerbForm
from .disease import DiseaseForm
from .ingredient import IngredientForm
from .prescription import PrescriptionForm
from .symptom import MMSymptomForm, TCMSymptomFrom
from .target import TargetForm
from .user import UserForm

_ = [
    DicTableDataForm,
    HerbForm,
    DiseaseForm,
    IngredientForm,
    PrescriptionForm,
    MMSymptomForm,
    TCMSymptomFrom,
    TargetForm,
    UserForm,
]
