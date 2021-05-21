"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: main_api_v2.py
@time: 2021/5/1 5:30 下午
@desc:
"""
import os

from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_login import current_user
from flask_security import auth_required
from loguru import logger

from application.controllers.common_model_opt import get_website_basic_info_dict
from application.controllers.main_apis_controllers import (
    get_projects,
    use_spacy_modal,
    extract_data_from_different_type_file,
    add_analyse_log,
    package_data_for_sandbox_v2,
    get_project_detail_v2,
    start_project_co,
    delete_project_co,
    exited_project_co,
    extract_data_from_database,
    package_tables_data_v2,
    extract_data_from_json, task_returner,
)
from application.utils.request_warpper import normal_api_wrapper
from config.settings import SWAGGER_FOLDER
from application.server.tasks import long_task

main_api_v2_bp = Blueprint("main_api_v2", __name__, url_prefix="/main/api/v2")


@main_api_v2_bp.route("/currentUser")
@auth_required()
def get_current_user():
    return jsonify(current_user.to_dict())


@main_api_v2_bp.route("/get_website_info")
@auth_required()
def get_website_info():
    basic = get_website_basic_info_dict()
    return jsonify(basic)


@main_api_v2_bp.route("/extractKnowledge", methods=["POST"])
@normal_api_wrapper
@swag_from(os.path.join(SWAGGER_FOLDER, "my_model_ner_message.yml"))
def extract_knowledge_from_message():
    """
    使用自训练模型处理
    :return:
    """
    return use_spacy_modal(request.json)


@main_api_v2_bp.route("/extract_from_table_file", methods=["POST"])
@normal_api_wrapper
def extract_from_table_file():
    files = request.files["files"]
    result = extract_data_from_different_type_file(files)
    return {"data": result}


@main_api_v2_bp.route("/extract_from_text", methods=["POST"])
@normal_api_wrapper
def extract_from_text():
    files = request.files["files"]
    result = extract_data_from_different_type_file(files)
    return {"data": result}


@main_api_v2_bp.route("/extract_from_json", methods=["POST"])
@normal_api_wrapper
def extract_from_json():
    files = request.files["files"]
    result = extract_data_from_different_type_file(files)
    if isinstance(result, list):
        return {"data": result}
    return {"data": [result]}


@main_api_v2_bp.route("/get_project_runtime")
@normal_api_wrapper
def get_project_runtime():
    """
    获取容器的运行状态
    Returns:

    """
    basic = get_projects(current_user.id)
    return basic


@main_api_v2_bp.route("/build_sandbox", methods=["POST"])
@auth_required()
@normal_api_wrapper
def build_sandbox():
    """
    data: [
        {
        'text': '矮地茶,艾叶,安息香',
        'annotations': [{"id":0,"label":1,"startOffset":20,"endOffset":24},...],
        'links': [{'rel_name':...,'left':...,'right':...},...]
        }
    ]
    projectName: ''
    projectDescription
    needEmail: ''
    """
    data = request.json
    if data["projectName"] == "":
        return {"msg": "Do you guys not have a name?"}
    data_list = package_data_for_sandbox_v2(data["data"])
    task = long_task.delay(
        data_list, data["projectName"], data["needEmail"], current_user.email
    )
    add_analyse_log(
        data, current_user, data["projectName"], task.id, data["projectDescription"]
    )
    return {"msg": "success", "task_id": task.id}
    # return jsonify({'code': 200, 'msg': 'success', 'data': create_sandbox()})


@main_api_v2_bp.route("/status/<task_id>")
@swag_from(os.path.join(SWAGGER_FOLDER, "query_tasks_status.yml"))
def taskstatus(task_id):
    """
    轮询任务进度
    TODO: 配合 creating 的查询标签测试
    """
    task = long_task.AsyncResult(task_id)
    try:
        response = task_returner(task)
        return jsonify(response)
    except Exception as _e:
        logger.exception(_e)
        return jsonify({"state": task.state})


@main_api_v2_bp.route("/show_project_detail/<task_id>")
@normal_api_wrapper
def show_project_detail(task_id):
    """

    Args:
        task_id:

    Returns:

    """
    project = get_project_detail_v2(task_id, current_user.id)
    if project.get("msg") == "no this project":
        raise Exception('no this project')
    return project


@main_api_v2_bp.route("/delete_project/<task_id>", methods=["DELETE"])
@normal_api_wrapper
@swag_from(os.path.join(SWAGGER_FOLDER, "delete_project.yml"))
def delete_project(task_id):
    """
    删除项目
    Args:
        task_id:

    Returns:

    """
    if delete_project_co(task_id, current_user.id):
        return {"msg": "operator success"}
    else:
        raise Exception('operation failed')


@main_api_v2_bp.route("/start_project/<task_id>")
@swag_from(os.path.join(SWAGGER_FOLDER, "start_project.yml"))
def start_project(task_id):
    """
    开始项目
    Args:
        task_id:

    Returns:

    """
    try:
        msg = start_project_co(task_id, current_user.id)
        if msg["code"] == 202:
            return jsonify(msg), 202
        elif msg["code"] == 200:
            return jsonify(msg)
        else:
            return jsonify(msg), 204
    except Exception as _e:
        logger.exception(_e)
        return jsonify({"code": -1, "msg": str(_e)}), 205


@main_api_v2_bp.route("/exited_project/<task_id>", methods=["PUT"])
@swag_from(os.path.join(SWAGGER_FOLDER, "exited_project.yml"))
def exited_project(task_id):
    """
    结束项目(休眠)
    Args:
        task_id:

    Returns:

    """
    try:
        msg = exited_project_co(task_id, current_user.id)
        return jsonify(msg)
    except Exception as _e:
        logger.exception(_e)
        return jsonify({"code": -1, "msg": str(_e)}), 205


@main_api_v2_bp.route("/knowledge_extract_from_database", methods=["POST"])
@normal_api_wrapper
def knowledge_extract_from_database():
    """
    结构化数据知识抽取的第二步
    表映射
    Returns:

    """
    config_data = request.json
    tables = extract_data_from_database(config_data, 1)
    return jsonify({"data": package_tables_data_v2(tables)})


@main_api_v2_bp.route("/knowledge_extract_from_json", methods=["POST"])
@normal_api_wrapper
def knowledge_extract_from_json():
    """
    半结构化数据知识抽取的第二步
    json <-> 数据表映射
    Returns:

    """
    data = request.json
    result = extract_data_from_json(data)
    return jsonify({"data": result})


@main_api_v2_bp.route("/build_sandbox_via_struct_data", methods=["POST"])
def build_sandbox_via_struct_data():
    """
    从结构化数据中构建sandbox
    Returns:

    """
    try:
        data = request.json
        if data["projectName"] == "":
            return jsonify({"code": -1, "msg": "Do you guys not have a name?"})
        task = long_task.delay(
            data["data"], data["projectName"], data["needEmail"], current_user.email
        )
        add_analyse_log(
            data,
            current_user,
            data["projectName"],
            task.id,
            data["projectDescription"],
            0,
        )
        return jsonify({"task_id": task.id}), 202
    except Exception as _e:
        logger.exception(_e)
        return jsonify({"code": -1, "msg": str(_e)})
