# -*- coding: utf-8 -*-
"""
    :time: 2021/1/26 16:47
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: common_model_opt.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
# from application.models import *
import importlib

from flask_sqlalchemy import Pagination

from application.models.herb import Herb
from application.models.prescription import Prescription

# from application.models.disease import Disease
from application.models.target import Target

# from application.models.dict_table import DicTableType, DicTableData
from application.models.ingredient import Ingredient

# from application.models.symptom import MMSymptom, TCMSymptom
# from application.models.authbase.role import Role
from application.models.authbase.user import User
from application.utils.data_management_reducer import (
    is_locked_field_in,
    get_cls_primary_key,
    check_model_name,
)


def query_data_from_models(
        cls: object, page: int, per_page: int, need_status: bool = True, condition=None
) -> Pagination:
    """

    Args:
        condition:
        cls:
        page:
        per_page:
        need_status:

    Returns:

    """
    if condition is None:
        condition = {}
    if need_status:
        res = cls.query.filter_by(i_status=1, **condition).paginate(
            page, int(per_page), error_out=False
        )
    else:
        res = cls.query.paginate(page, int(per_page), error_out=False)
    return res


def data_query(post_data: dict):
    """

    Args:
        post_data:

    Returns:

    """
    type_ = post_data["type_"]
    draw = post_data.get("draw", 0)
    not_need_status_list = ["Role", "User"]

    if not check_model_name(type_):
        return {"draw": draw, "recordsTotal": 0, "recordsFiltered": 0, "data": []}

    per_page = int(post_data.get("length", 10))
    page = int(int(post_data.get("start", 0)) / per_page) + 1
    search = post_data.get("search[value]", None)
    if per_page in [10, 25, 50, 100]:
        tmp_cls = importlib.import_module("application.models", type_)
        cls = getattr(tmp_cls, type_)
        # cls = eval(type_ + "()")
        if not search:
            res = query_data_from_models(
                cls, page, per_page, type_ not in not_need_status_list
            )
        else:
            res = cls.query.filter_by(s_name=search, i_status=1).paginate(
                int(page), int(per_page), error_out=False
            )
        ret = {
            "draw": int(draw),
            "recordsTotal": res.total,
            "recordsFiltered": res.total,
            "data": [foo.to_dict() for foo in res.items],
        }
        return ret
    else:
        return {"draw": draw, "recordsTotal": 0, "recordsFiltered": 0, "data": []}


def data_query_particular(data: str, cls_str: str) -> dict:
    """

    Args:
        data: id
        cls_str: type

    Returns:

    """
    if not check_model_name(cls_str):
        return {}
    id_field = get_cls_primary_key(cls_str)
    query_data = {id_field: data, "i_status": 1}

    tmp_cls = importlib.import_module("application.models", cls_str)
    cls = getattr(tmp_cls, cls_str)

    query_res = cls.query.filter_by(**query_data).first()
    if query_res:
        return query_res.to_dict_particular()


def data_create(data: dict, cls_str: str) -> str:
    """

    Args:
        cls_str:
        data:

    Returns:

    """
    if "s_name" not in data:
        return "loss necessary field"
    if not check_model_name(cls_str):
        return "invalid model"

    tmp_cls = importlib.import_module("application.models", cls_str)
    cls = getattr(tmp_cls, cls_str)

    query_res = cls.query.filter_by(s_name=data["s_name"]).first()
    if query_res:
        return "data with the name has existed"
    else:
        cls = cls()
        if is_locked_field_in(data, cls):
            return "what the fucking data?"
        cls.add(data)
        return "add success"


def data_delete(data: str, cls_str: str) -> str:
    """
    根据id删
    Args:
        cls_str:
        data: id

    Returns:

    """
    if not check_model_name(cls_str):
        return "invalid model"
    data_for_del = {get_cls_primary_key(cls_str): data}

    tmp_cls = importlib.import_module("application.models", cls_str)
    cls = getattr(tmp_cls, cls_str)

    query_res = cls.query.filter_by(**data_for_del).first()
    if query_res and query_res.i_status == 1:
        query_res.fake_delete()
        return "delete success"
    else:
        return "this value(name) is not in the database"


def data_update(data: dict, cls_str: str) -> str:
    """
    根据名字改，后期改成根据id改
    Args:
        cls_str:
        data:

    Returns:

    """
    if not check_model_name(cls_str):
        return "invalid model"

    pk = get_cls_primary_key(cls_str)
    if "id" in data:
        query = {pk: data.pop("id"), "i_status": 1}

        tmp_cls = importlib.import_module("application.models", cls_str)
        cls = getattr(tmp_cls, cls_str)

        query_res = cls.query.filter_by(**query).first()
        if query_res:
            if is_locked_field_in(data, query_res):
                return "what the fucking data?"
            query_res.update(data)
            return "update success"
        else:
            return "this value(name) is not in the database"
    else:
        return "fucking query"


def get_website_basic_info_dict() -> dict:
    """
    获取网站的基本信息
    Returns:

    """

    user_count = User.query.filter_by().count()
    herb_count = Herb.query.filter_by().count()
    prescription_count = Prescription.query.filter_by().count()
    gene_count = Target.query.filter_by().count()
    protein_count = Ingredient.query.filter_by().count()
    other_count = 1742 + 956
    count = herb_count + protein_count + prescription_count + gene_count
    return {
        "user_c": user_count,
        "total_c": count + other_count,
        "herb_c": herb_count,
        "pre_c": prescription_count,
        "gene_c": gene_count,
        "pro_c": protein_count,
        "other_c": other_count,
    }
