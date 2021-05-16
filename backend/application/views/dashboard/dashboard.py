"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: dashboard.py
@time: 2021/1/26 21:00
@desc:
"""
from flask import Blueprint, render_template, request, jsonify
from flask_security import roles_required
from loguru import logger

from application.controllers.dashboard_datamanage import (
    query_data_controller,
    create_data_controller,
    switch_type_title,
    get_data_table_fields,
    check_page_style,
)
from application.controllers.dashboard_main import docker_neo4j_list

dash_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dash_bp.route("/")
@roles_required("admin")
def dashboard_index():
    neo_list = docker_neo4j_list()
    return render_template("dashboard/index.html", neo_list=neo_list)


@dash_bp.route("/show_herb_data_table")
def show_herb_data_table():
    """
    展示herb数据
    Returns:

    """
    page_type = request.args.get("type")
    title = switch_type_title(page_type)
    fields = get_data_table_fields(page_type)
    page_style = check_page_style(page_type)
    return render_template(
        "dashboard/data_management/herb_show.html",
        title=title,
        subtitle=title + "数据",
        fields=fields,
        page_type=page_style,
    )
    # return render_template('dashboard/data_management/datatable_demo.html')


@dash_bp.route("/query_particular", methods=["POST"])
def query_particular():
    """
    查询具体的数据
    Returns:

    """
    data = request.json or (request.form and request.data)

    try:
        form = query_data_controller(data)
        if form:
            return jsonify(
                {
                    "code": 200,
                    "msg": render_template(
                        "dashboard/data_management/query_herb_form.html", form=form
                    ),
                }
            )
        else:
            return jsonify({"code": -1, "msg": "not find"})
    except Exception as _e:
        logger.error(f"{_e}, raw data: {data}")
        return jsonify({"code": -1, "msg": f"error {_e}"})


@dash_bp.route("/edit_particular", methods=["POST"])
def edit_particular():
    """
    修改数据
    Returns:

    """
    data = request.json or (request.form and request.data)

    try:
        form = query_data_controller(data)
        if form:
            return jsonify(
                {
                    "code": 200,
                    "msg": render_template(
                        "dashboard/data_management/edit_herb_form.html", form=form
                    ),
                }
            )
    except Exception as _e:
        logger.error(f"{_e}, raw data: {data}")
        return jsonify({"code": -1, "msg": f"error {_e}"})


@dash_bp.route("/create_particular", methods=["POST"])
def create_particular():
    """
    新增数据
    Returns:

    """
    data = request.json or (request.form and request.data)
    try:
        form = create_data_controller(data)
        return jsonify(
            {
                "code": 200,
                "msg": render_template(
                    "dashboard/data_management/create_herb_form.html", form=form
                ),
            }
        )
    except Exception as _e:
        logger.error(f"{_e}, raw data: {data}")
        return jsonify({"code": -1, "msg": f"error {_e}"})
