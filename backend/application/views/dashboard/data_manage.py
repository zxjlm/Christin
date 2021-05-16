# -*- coding: utf-8 -*-
"""
    :time: 2021/1/27 16:03
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: data_manage.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import Blueprint, request, jsonify
from flask_security import roles_required
from loguru import logger

from application.controllers.common_model_opt import (
    data_create,
    data_delete,
    data_update,
    data_query,
    data_query_particular,
)
from application.controllers.dashboard_datamanage import get_data_table_fields
from application.utils.docker_handler import get_all_container_and_classify
from application.utils.custom_exceptions import (
    UnknownValueException,
    Neo4jUpdateFailedException,
)

dm_bp = Blueprint("data_manage", __name__, url_prefix="/api/v1")


@dm_bp.route("/query", methods=["POST"])
@roles_required("admin")
def query():
    try:
        res = data_query(request.form)
        return jsonify(res)
    except Exception as _e:
        logger.exception(_e)
        logger.error("{}, raw data: {}".format(_e, request.form.to_dict()))
        return jsonify(
            {"draw": -1, "recordsTotal": -1, "recordsFiltered": -1, "data": []}
        )


# @dm_bp.route('/query_user', method=['POST'])
# def query_user():
#     try:
#         res = data_query_for_user()
#         return jsonify(res)
#     except Exception as _e:
#         logger.exception(_e)
#         logger.error("")
#         return jsonify(
#             {"draw": -1, "recordsTotal": -1,
#             "recordsFiltered": -1, "data": []}
#         )


@dm_bp.route("/query_particular", methods=["POST"])
@roles_required("admin")
def query_particular():
    data = request.json or (request.form and request.data)
    try:
        msg = data_query_particular(data["data"], data["type"])
        if msg:
            return jsonify({"code": 200, "msg": msg})
        else:
            return jsonify({"code": -1, "msg": "not find"})
    except Exception as _e:
        logger.error(f"{_e}, raw data: {data}")
        return jsonify({"code": -1, "msg": f"error {_e}"})


@dm_bp.route("/create", methods=["POST"])
@roles_required("admin")
def create():
    """

    Returns:

    """
    data = request.json or (request.form and request.data)
    try:
        msg = data_create(data["data"], data["type"])
        return jsonify({"code": 200, "msg": msg})
    except Exception as _e:
        logger.error(f"{_e}, raw data: {data}")
        return jsonify({"code": -1, "msg": f"error {_e}"})


@dm_bp.route("/delete", methods=["POST"])
@roles_required("admin")
def delete():
    """

    Returns:

    """
    data = request.json or (request.form and request.data)
    try:
        msg = data_delete(data["data"], data["type"])
        return jsonify({"code": 200, "msg": msg})
    except Exception as _e:
        logger.error(f"{_e}, raw data: {data}")
        return jsonify({"code": -1, "msg": f"error {_e}"})


@dm_bp.route("/update", methods=["POST"])
@roles_required("admin")
def update():
    """

    Returns:

    """
    data = request.json or (request.form and request.data)
    try:
        msg = data_update(data["data"], data["type"])
        return jsonify({"code": 200, "msg": msg})
    except UnknownValueException as _:
        logger.error(
            f" {request.remote_addr} push a unknown data, raw data: {data}, value: {_}"
        )
        return jsonify({"code": -1, "msg": "unknown value used"})
    except Neo4jUpdateFailedException as nuf_e:
        logger.exception(nuf_e)
        return jsonify({"code": -1, "msg": f"neo4j update failed, error {nuf_e}"})
    except Exception as _e:
        logger.error(f"{_e}, raw data: {data}")
        return jsonify({"code": -1, "msg": f"error {_e}"})


@dm_bp.route("/get_dt_fields")
@roles_required("admin")
def get_dt_fields():
    type_ = request.args.get("type")
    res = get_data_table_fields(type_)
    return jsonify({"code": 200, "msg": res})


@dm_bp.route("/show_docker_containers")
def show_docker_containers():
    res = get_all_container_and_classify()
    return res
