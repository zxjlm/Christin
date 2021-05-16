# -*- coding: utf-8 -*-
"""
    :time: 2021/2/20 16:10
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: dashboard_datamanage.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import importlib

from application.controllers.common_model_opt import data_query_particular


def query_data_controller(data):
    msg = data_query_particular(data["data"], data["type"])
    if msg:
        tmp_cls = importlib.import_module("application.forms", data["type"] + "Form")
        form = getattr(tmp_cls, data["type"] + "Form")()
        for k, v in msg.items():
            setattr(getattr(form, k), "data", v)
        return form
    else:
        return False


def create_data_controller(data):
    # from application.forms.dict_table_data import DicTableDataForm
    # from application.forms.herb import HerbForm
    # from application.forms.target import TargetForm
    # from application.forms.symptom import MMSymptomForm, TCMSymptom
    # from application.forms.disease import DiseaseForm
    # from application.forms.ingredient import IngredientForm
    # from application.forms.prescription import PrescriptionForm
    tmp_cls = importlib.import_module("application.forms", data["type"] + "Form")

    form = getattr(tmp_cls, data["type"] + "Form")()
    delattr(form, "id")
    return form


def switch_type_title(type_: str) -> str:
    """
    输出该类型所对应的标题组
    Args:
        type_:

    Returns:

    """
    ret = {
        "Herb": "中药",
        "Prescription": "处方",
        "Disease": "疾病",
        "Ingredient": "中药组成",
        "MMSymptom": "症状(MM)",
        "TCMSymptom": "症状(TCM)",
        "Target": "基因",
        "DicTableData": "字典表",
        "LoginData": "登录记录",
        "User": "用户数据",
        "Role": "角色数据",
    }
    return ret.get(type_, "")


def check_page_style(type_: str) -> int:
    """
    检查页面的样式风格
    Args:
        type_:

    Returns:

    """
    dic = {1: ["User", "LoginData"]}  # 不可手动添加
    for k, v in dic.items():
        if type_ in v:
            return k
    return 0


def get_data_table_fields(type_):
    """
    获取数据表需要展示的字段
    Args:
        type_:

    Returns:

    """
    # if type_ == 'Herb':
    #     from application.models.herb.herb import Herb
    #     return Herb.data_table_fields()
    # elif type_ == 'Prescription':
    #     from application.models.prescription.prescription import Prescription
    #     return Prescription.data_table_fields()
    # elif type_ == 'Role' or type_ == 'User':
    #     mod = importlib.import_module('application.models.authbase', type_)
    # else:
    #     mod = importlib.import_module('applicatino.models.')
    mod = importlib.import_module("application.models", type_)
    return getattr(mod, type_).data_table_fields()
