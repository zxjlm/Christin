"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: main.py
@time: 2021/1/3 23:23
@desc:
"""
from flask import Blueprint, render_template, jsonify, redirect, url_for, request
from flask_security import auth_required, current_user

from application.controllers.common_model_opt import get_website_basic_info_dict
from application.controllers.main_apis_controllers import (
    get_neo_config,
    get_projects,
    get_project_detail,
    query_neo_nodes,
    count_projects,
)
from config.settings import NEO_HOST

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@auth_required()
def index():
    basic = get_website_basic_info_dict()

    all_projects = get_projects(current_user.id)
    count = count_projects(all_projects)
    return render_template("index.html", basic=basic, count=count)


@main_bp.route("/create_project")
def create_project():
    return render_template("create_project.html")


@main_bp.route("/projects")
@auth_required()
def projects():
    all_projects = get_projects(current_user.id)
    count = count_projects(all_projects)
    return render_template("projects.html", projects=all_projects, count=count)


@main_bp.route("/query_graph", methods=["GET", "POST"])
def query_graph():
    """
    查询图数据
    Returns:

    """
    return render_template("visneo/vis_neo.html")


@main_bp.route("/return_neo_page/<task_id>")
def neo_page(task_id):
    """
    {
    'port': 7791,
    'task_id': '512cfa3c-2434-4c8c-9db4-0e3075a93df6',
    'password': 'IUk2ZKeI',
    'container_id': '.......'}
    Args:
        task_id:

    Returns:

    """
    config = get_neo_config(task_id)
    return render_template(
        "visneo/vis_neo.html", password=config["password"], port=config["port"]
    )


@main_bp.route("/show_project_detail/<task_id>")
def show_project_detail(task_id):
    """

    Args:
        task_id:

    Returns:

    """
    project = get_project_detail(task_id, current_user.id)
    if "msg" in project:
        return ""
    return jsonify(
        {
            "html": render_template("project_detail.html", project=project),
            "data": project["data"],
        }
    )


@main_bp.route("/neo_vis/<task_id>")
def neo_vis(task_id):
    """

    Args:
        task_id:

    Returns:

    """
    project = get_project_detail(task_id, current_user.id)
    return redirect(
        url_for(
            "main.neovis_page",
            port=project["remark"]["port"],
            pwd=project["remark"]["password"],
        )
    )


@main_bp.route("/neo-page/<port>/<pwd>")
def neovis_page(port, pwd):
    """
    渲染neovis页面
    Args:
        port:
        pwd:

    Returns:

    """
    nodes = query_neo_nodes(port, pwd)
    node_name = list(nodes.values())
    return render_template(
        "visneo/vis_neo.html",
        pwd=pwd,
        port=port,
        nodes=nodes,
        node_name=node_name,
        neo_host=NEO_HOST,
    )


@main_bp.route("/get_struct_data_modal")
def get_struct_data_modal():
    data = request.args.get("modal")
    if data == "strict":
        return render_template("create_project/create_project_struct.html")
    elif data == "half":
        return render_template("create_project/create_project_half_struct.html")
    else:
        return render_template("create_project/create_project_normal.html")


# @main_bp.route("/test/<port>/<pwd>")
# def test(port, pwd):
#     """
#
#     Returns:
#
#     """
#     return render_template("./ant-neo/index.html")


@main_bp.route("/testdata/test-list.json")
def test_data_autocomplete():
    return jsonify(["111", "222"])
