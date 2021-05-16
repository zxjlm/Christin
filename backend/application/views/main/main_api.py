# -*- coding: utf-8 -*-
"""
    :time: 2021/2/9 11:03
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: main_api.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import os
import time

from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_login import current_user
from flask_security import auth_required
from loguru import logger

from application.controllers.main_apis_controllers import (
    u_my_model,
    generate_fake_data,
    u_normal_model,
    add_analyse_log,
    delete_project_co,
    start_project_co,
    extract_data_from_file,
    extract_data_from_database,
    package_tables_data,
    extract_data_from_json_file_v1,
    package_data_for_sandbox,
)
from application.extensions import apicode
from application.server.tasks import long_task_for_test, long_task
from config.settings import SWAGGER_FOLDER

main_api_bp = Blueprint("main_api", __name__, url_prefix="/main/api/v1")


@main_api_bp.route("/status/<task_id>")
@swag_from(os.path.join(SWAGGER_FOLDER, "query_tasks_status.yml"))
def taskstatus(task_id):
    """
    轮询任务进度
    TODO: 配合 creating 的查询标签测试
    """
    task = long_task_for_test.AsyncResult(task_id)
    if task.state == "PENDING":
        response = {
            "state": "empty task",
            "info": {"current": 0, "total": 4, "status": "empty task"},
        }
    elif task.state == "FILL DATA":
        # r = redis.Redis(host=REDIS_HOST, port=6379, db=1)
        # success_list = get_all_data_from_redis_list(r,
        #                                             task_id +
        #                                             "-midway-success")
        # logger.info("success {}".format(",".join(success_list)))
        # failed_list = get_all_data_from_redis_list(r,
        #                                            task_id + "-midway-failed")
        response = {
            "state": task.state,
            "info": task.info,
            "success_list": [],
            "failed_list": [],
        }
    elif task.state == "SUCCESS":
        # msg = update_analyse_log(task.info['config'], task_id)
        response = {"state": task.state, "info": task.info, "msg": "success"}
        if "result" in task.info:
            response["result"] = task.info["result"]
    elif task.state != "FAILURE":
        response = {"state": task.state, "info": task.info}
        if "result" in task.info:
            response["result"] = task.info["result"]
    else:
        # something went wrong in the background job
        response = {
            "state": task.state,
            "info": {
                "current": 4,
                "total": 4,
            },
            "status": str(task.info),  # this is the exception raised
        }
    try:
        return jsonify(response)
    except Exception as _e:
        logger.exception(_e)
        return jsonify({"state": task.state})


@main_api_bp.route("/my_model", methods=["POST"])
@swag_from(os.path.join(SWAGGER_FOLDER, "my_model_ner_message.yml"))
def my_model():
    """
    使用自训练模型处理
    :return:
    """
    time.sleep(2)
    if request.json and request.json.get("message"):
        message = request.json["message"]
    else:
        return jsonify(apicode.missingparameters)
    try:
        return jsonify({"code": 200, "msg": "success", "data": u_my_model(message)})
    except Exception as _e:
        logger.warning(f"my model error, {message}, {_e}")
        return jsonify(apicode.dataanalyzeunknownerror)


@main_api_bp.route("/my_model_file", methods=["POST"])
@swag_from(os.path.join(SWAGGER_FOLDER, "my_model.yml"))
def my_model_file():
    """
    根据我自己训练的NER模型进行提取
    Returns:

    """
    time.sleep(2)
    try:
        if request.files:
            file = request.files["file"]
            msg_dict = extract_data_from_file(file)
            return jsonify({"code": 200, **msg_dict})
        else:
            return jsonify({"code": -1, "msg": "no file"})
    except UnicodeDecodeError as _ude:
        return jsonify({"code": -1, "msg": f"please change code to utf-8, {_ude}"})
    except Exception as _e:
        return jsonify({"code": -1, "msg": f"Unknown Error, {_e}"})


@main_api_bp.route("/fake_model", methods=["POST"])
def fake_model():
    """
    假接口,返回固定的值
    """
    time.sleep(2)
    return jsonify({"code": 200, "msg": "success", "data": generate_fake_data()})


@main_api_bp.route("/normal_model", methods=["POST"])
def normal_model():
    """
    使用通用模型处理(仅仅演示用)

    选择使用的模型:undo
    :return:
    """

    message = request.json["message"]

    return jsonify({"code": 200, "msg": "success", "data": u_normal_model(message)})


@main_api_bp.route("/api/build_sandbox", methods=["POST"])
@auth_required()
def build_sandbox():
    """
    data_list: [
        {'text': '矮地茶,艾叶,安息香',
        'ents': [[0, 3, 'HERB'], [4, 6, 'HERB'], [7, 10, 'HERB']],
        'links': [{'rel_name':...,'left':...,'right':...},...]
        }
    ]
    project_name: ''
    """
    try:
        data = request.json
        if data["project_name"] == "":
            return jsonify({"code": -1, "msg": "Do you guys not have a name?"})
        data_list = package_data_for_sandbox(data["data_list"])
        task = long_task.delay(
            data_list, data["project_name"], data["need_email"], current_user.email
        )
        add_analyse_log(
            data, current_user, data["project_name"], task.id, data["description"]
        )
        return jsonify({"code": 200, "msg": "success", "task_id": task.id}), 202
    except Exception as _e:
        logger.exception(_e)
        return jsonify({"code": -1, "msg": str(_e)})
    # return jsonify({'code': 200, 'msg': 'success', 'data': create_sandbox()})


@main_api_bp.route("/delete_project/<task_id>", methods=["DELETE"])
@swag_from(os.path.join(SWAGGER_FOLDER, "delete_project.yml"))
def delete_project(task_id):
    """

    Args:
        task_id:

    Returns:

    """
    try:
        if delete_project_co(task_id, current_user.id):
            return jsonify({"code": 200, "msg": "operator success"})
        else:
            return jsonify({"code": 201, "msg": "operator failed"})
    except Exception as _e:
        logger.exception(_e)
        return jsonify({"code": -1, "msg": str(_e)})


@main_api_bp.route("/start_project/<task_id>")
@swag_from(os.path.join(SWAGGER_FOLDER, "start_project.yml"))
def start_project(task_id):
    """

    Args:
        task_id:

    Returns:

    """
    try:
        msg = start_project_co(task_id, current_user.id)
        if msg["code"] == 202:
            return jsonify(msg), 202
        else:
            return jsonify(msg)
    except Exception as _e:
        logger.exception(_e)
        return jsonify({"code": -1, "msg": str(_e)})


@main_api_bp.route("/knowledge_extract_from_database", methods=["POST"])
def knowledge_extract_from_database():
    try:
        config_data = request.json
        tables = extract_data_from_database(config_data)
        res = package_tables_data(tables)
        return jsonify({"code": 200, "msg": "success", **res})
    except Exception as _e:
        return jsonify({"code": -1, "msg": str(_e)})


@main_api_bp.route("/knowledge_extract_from_json_file", methods=["POST"])
def knowledge_extract_from_json_file():
    try:
        res = extract_data_from_json_file_v1(request.files)
        return jsonify({"code": 200, "msg": "success", "data": res})
    except Exception as _e:
        return jsonify({"code": -1, "msg": str(_e)})
