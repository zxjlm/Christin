"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: main_apis_controllers.py
@time: 2021/1/16 23:04
@desc:
"""
import importlib
import json
import time

import docker
import spacy
from py2neo import Graph, NodeMatcher
from spacy import displacy
import pandas as pd
import chardet
from werkzeug.datastructures import MultiDict

from application.models import Labels
from application.models.authbase import AnalysesLog
from application.server.tasks import neo_start, long_task
from application.utils.file_handler import (
    extract_data_from_csv_file,
    extract_data_from_excel_file,
    extract_data_from_text_file,
    parser_json_file_v1,
    extract_data_from_json_file,
)
from application.utils.mysql_handler import (
    generate_validate_query,
    mysql_query_operator,
)
from application.utils.nlp_render import my_json_render, doccano_wapper
from application.utils.normal import (
    get_random_color,
    get_time_delta,
    unique_list_dict_via_one_key,
)
from config.settings import NEO_HOST, ROOT_PATH


def u_my_model(message: str):
    """

    Args:
        message: 待分析的语句

    Returns:

    """
    nlp = spacy.load("./application/nlp_model")
    res = []
    for msg in message.split("\n\n"):
        doc = nlp(msg)
        json_result = my_json_render(
            doc, style="ent", options={"colors": {"ZZ": "#B0A137"}}
        )
        res += json_result
    return res


def get_messages_for_ner_model(request_json: dict):
    """
    将前端传回的数据做预处理,提取需要的数据
    总共分为三类: message |  text-file  |  excel-or-csv-file
    Returns:

    """
    results = []
    message = request_json.get("message", [])
    texts = request_json.get("text-file", [])
    tables = request_json.get("excel-or-csv-file", [])
    if message:
        results += request_json["message"].split("\n\n")
    for text in texts:
        if text.get("response") and text["response"].get("data"):
            results += text["response"]["data"]
    for table in tables:
        if table.get("response") and table["response"].get("data"):
            results += table["response"]["data"]
    return results


def use_spacy_modal(request_json: dict):
    """

    Args:
        request_json: 前端传回的数据

    Returns:

    """
    nlp = spacy.load(ROOT_PATH + "/application/nlp_model")
    res = []
    messages = get_messages_for_ner_model(request_json)
    for msg in messages:
        doc = nlp(msg)
        json_result = my_json_render(
            doc, style="ent", options={"colors": {"ZZ": "#B0A137"}}
        )
        res += json_result
    return doccano_wapper(res)


def u_normal_model(message):
    """

    Args:
        message:待分析的语句

    Returns:

    """
    nlp = spacy.load("zh_core_web_md")
    doc = nlp(message)
    html = displacy.render(doc, style="ent")
    return html


def package_data_for_sandbox(data_list: list) -> dict:
    """

    Args:
        data_list:[
        {'text': '矮地茶,艾叶,安息香',
        'ents': [[0, 3, 'HERB'], [4, 6, 'HERB'], [7, 10, 'HERB']],
        'links': [{'rel_name':...,'left':...,'right':...},...]
        }
    ]

    Returns:{
            nodes:[]
            relationships:[]
        }

    """
    result = {"nodes": [], "relationships": []}
    for data in data_list:
        result["nodes"] += [
            {"name": data["text"][ent[0]: ent[1]], "type": ent[2]}
            for ent in data["ents"]
        ]
        result["relationships"] += data["links"]
    return result


def package_data_for_sandbox_v2(data_list: list) -> dict:
    """

    Args:
        data_list:[
        {
        'text': '矮地茶,艾叶,安息香',
        'annotations': [{"id":0,"label":1,"startOffset":20,"endOffset":24},...],
        'links': [{'rel_name':...,'left':...,'right':...},...]
        }
    ]

    Returns:{
            nodes:[]
            relationships:[]
        }

    """
    result = {"nodes": [], "relationships": []}
    for data in data_list:
        for annotation in data["annotations"]:
            label = Labels.query.get(annotation["label"])
            if label:
                result["nodes"].append(
                    {
                        "name": data["text"][
                                annotation["startOffset"]: annotation["endOffset"]
                                ],
                        "type": label.s_name,
                    }
                )
        # result["relationships"] += data["links"]
    return result


def generate_fake_data():
    """
    返回假数据
    """
    # graph = Graph(SecureInfo.get_neo4j_blot(),
    #               password=SecureInfo.get_neo4j_password())
    # node_query = graph.run("MATCH (n:Herb) RETURN n LIMIT 3;")
    # nodes = node_query.data()
    # text = ','.join([node['n']['s_name'] for node in nodes])
    # data = []
    # start = 0
    # for foo in nodes:
    #     ent = {'label': 'HERB', 'start': start,
    #            'end': start + len(foo['n']['s_name'])}
    #     start += len(foo['n']['s_name']) + 1
    #     data.append(ent)

    # return [{'text': text, 'ents': data}]
    return [
        {
            "text": "测试方:矮地茶,艾叶,安息香.",
            "ents": [
                {"label": "PRESCRIPTION", "start": 0, "end": 3},
                {"label": "HERB", "start": 4, "end": 7},
                {"label": "HERB", "start": 8, "end": 10},
                {"label": "HERB", "start": 11, "end": 14},
            ],
        }
    ]


def create_sandbox():
    """
    创建sandbox
    """
    ...


def push_sandbox_data(data_list: list):
    """
    将sandbox的启动节点推入各自的mysql
    Returns:

    """
    # 首先是将分析的数据推入节点划分的记录数据库（mongoDB?） 这个可以暂时先不搞
    # 其次是将划分的结果推入节点数据库
    pass


def add_analyse_log(
        data: dict,
        user: str,
        project_name: str,
        task_id: str,
        description: str,
        analyse_type: int = 2,
):
    """
    记录操作的数据
    Args:
        analyse_type: 分析类型
        data: 操作的原数据
        user: 操作人
        project_name: 项目名称
        task_id: 任务id
        description: 项目描述

    Returns:

    """
    ana = AnalysesLog()
    ana.add(
        {
            "data": data,
            "current_user": user,
            "s_project_name": project_name,
            "s_mark": task_id,
            "s_project_description": description,
            "i_analysis_type": analyse_type,
        }
    )


def update_analyse_log(data, task_id):
    """
    在neo建立完毕之后更新数据库
    Args:
        data:
        task_id:

    Returns:

    """
    ana = AnalysesLog.query.filter_by(s_mark=task_id).first()
    if ana:
        ana.update({"j_remark": data, "i_status": 1})
        return "update db success"
    else:
        return "invalid container_id"


def get_neo_config(task_id):
    ana = AnalysesLog.query.filter_by(s_mark=task_id).first()
    return ana.j_remark


def get_projects(user_id: str) -> dict:
    """
    获取项目并更新
    Args:
        user_id:

    Returns:
        {
            running: [...],
            exited: [...],
            ...
        }

    """
    mapper = AnalysesLog.get_mapper()

    client = docker.from_env()
    containers = {
        container.name: container.status
        for container in client.containers.list(all=True)
    }
    projects = AnalysesLog.query.filter_by(s_sy_user_id=user_id).all()
    for project in projects:
        flag = containers.get(project.s_mark, "exited") != "exited"
        if project.i_status == 3 and flag:
            continue
        elif project.s_mark in containers:
            status = containers[project.s_mark]
            project.update({"i_status": mapper.index(status)})
        else:
            project.update({"i_status": 0})

    projects_dict = {"creating": [], "running": [], "exited": [], "deleted": []}
    for project in projects:
        tmp = project.to_dict()
        tmp["suffix"] = tmp["s_project_name"][:2]
        # 着色
        time_delta = get_time_delta(tmp["update_date_time"])
        if time_delta > 10:
            tmp["badge_color"] = "danger"
        elif time_delta > 3:
            tmp["badge_color"] = "warning"
        else:
            tmp["badge_color"] = "info"
        tmp["suffix_color"] = get_random_color()
        projects_dict[tmp["status"]].append(tmp)

    return projects_dict


def count_projects(proj: dict) -> dict:
    """
    计算项目的数量
    Args:
        proj:

    Returns:

    """
    res = {}
    for k, v in proj.items():
        res[k] = len(v)
    return res


def get_project_detail(task_id, userid) -> dict:
    project = AnalysesLog.query.filter_by(s_mark=task_id, s_sy_user_id=userid).first()
    if project:
        res = project.to_dict_particular()
        data_ana = json.loads(res["data"])  # 数据源,渲染为标注card
        for ind, foo in enumerate(data_ana["data_list"]):
            for idx, ent in enumerate(foo["ents"]):
                data_ana["data_list"][ind]["ents"][idx] = {
                    "start": ent[0],
                    "end": ent[1] + 1,
                    "label": ent[2],
                }
        res["data"] = data_ana["data_list"]
        remark = res["remark"]
        res["remark"] = {
            "port": remark["port"],
            "password": remark["password"],
        }  # port\password
        return res
    else:
        return {"msg": "no this project"}


def get_project_detail_v2(task_id, userid) -> dict:
    project = AnalysesLog.query.filter_by(s_mark=task_id, s_sy_user_id=userid).first()
    labels = [foo.to_config() for foo in Labels.query.all()]
    if project:
        res = project.to_dict_particular()
        res["data"] = json.loads(res["data"])["data"]
        res["labels"] = labels
        if project.i_status != 3:
            remark = res["remark"]
            res["remark"] = {
                "port": remark["port"],
                "password": remark["password"],
            }  # port\password
        return res
    else:
        return {"msg": "no this project"}


def delete_project_co(task_id, userid):
    """

    Args:
        task_id:
        userid:

    Returns:

    """
    project = AnalysesLog.query.filter_by(s_mark=task_id, s_sy_user_id=userid).first()
    if project:
        client = docker.from_env()
        containers = {
            container.name: container for container in client.containers.list(all=True)
        }
        if task_id in containers:
            container = containers[task_id]
            if container.status == "running":
                container.stop()
                time.sleep(2)
                container.remove()
            elif container.status == "exited":
                container.remove()
            else:
                pass
        project.update({"i_status": 0})
        return {"code": 200, "msg": "delete success"}
    else:
        return {"code": -1, "msg": "unknown project"}


def start_project_co(task_id, userid):
    """
    开启项目容器
    Args:
        task_id:
        userid:

    Returns:

    """
    project = AnalysesLog.query.filter_by(s_mark=task_id, s_sy_user_id=userid).first()
    if project:
        client = docker.from_env()
        containers = {
            container.name: container for container in client.containers.list(all=True)
        }
        if task_id in containers:
            container = containers[task_id]
            if container.status == "running":
                project.update({"i_status": 0})
                return {"code": 200, "msg": "project is running", "task_id": "-1"}
            elif container.status == "exited":
                task = neo_start.delay(
                    task_id,
                    project.s_project_name,
                    int(project.j_remark["port"]),
                    project.j_remark["password"],
                )
                return {"code": 202, "msg": "success", "task_id": task.id}
            else:
                project.update({"i_status": 0})
        else:
            return {"code": -1, "msg": "check project status first"}
    else:
        return {"code": -1, "msg": "shabi"}


def exited_project_co(task_id, userid):
    """

    Returns:

    """
    project = AnalysesLog.query.filter_by(s_mark=task_id, s_sy_user_id=userid).first()
    if project:
        client = docker.from_env()
        containers = {
            container.name: container for container in client.containers.list(all=True)
        }
        if task_id in containers:
            container = containers[task_id]
            if container.status == "running":
                time.sleep(5)
                container.stop()
            else:
                return {"msg": "invalid operator"}
        project.update({"i_status": 2})
        return {"msg": "exited success"}
    else:
        return {"msg": "unknown project"}


def extract_data_from_file(file) -> dict:
    """
    从输入流中提取数据,并导入识别模型
    Args:
        file:

    Returns:
        返回一个包含了状态信息的结果字典
    """
    nlp = spacy.load("./application/nlp_model")
    res = []
    if file.mimetype == "text/csv":
        df = pd.read_csv(file)
        for idx in df.index:
            doc = nlp(df.loc[idx, "data"])
            json_result = my_json_render(
                doc, style="ent", options={"colors": {"ZZ": "#B0A137"}}
            )
            res += json_result
    elif file.mimetype == "application/octet-stream":
        pass  # numbers
    elif (
            file.mimetype == "application/vnd.openxmlformats"
                             "-officedocument.spreadsheetml.sheet"
    ):
        df = pd.read_excel(file, engine="openpyxl")
        for idx in df.index:
            doc = nlp(df.loc[idx, "data"])
            json_result = my_json_render(
                doc, style="ent", options={"colors": {"ZZ": "#B0A137"}}
            )
            res += json_result
    elif file.mimetype == "text/plain":
        file_data = file.read()
        if chardet.detect(file_data)["encoding"] == "GB2312":
            file_data = file_data.decode("gbk")
        else:
            file_data = file_data.decode()
        for msg in file_data.split("\n"):
            doc = nlp(msg)
            json_result = my_json_render(
                doc, style="ent", options={"colors": {"ZZ": "#B0A137"}}
            )
            res += json_result
    else:
        pass

    return {"msg": "success", "data": res}


def query_neo_nodes(port, pwd):
    """
    查询所有的节点
    Args:
        port:
        pwd:

    Returns:

    """
    graph = Graph(f"bolt://{NEO_HOST}:" + port, password=pwd)
    nodes_matcher = NodeMatcher(graph)
    nodes = list(nodes_matcher.match())
    return {node.identity: node["s_name"] for node in nodes}


def extract_data_from_database(config, data_number: int = -1):
    """
    从数据库中提取数据
    Args:
        data_number: 需要提取多少条数据
        config:

    Returns:

    """
    sql_generator = generate_validate_query()
    tables = []
    for sql, fields, table_name in sql_generator:
        results = []
        data, cols = mysql_query_operator(
            config["db-host"],
            config["db-port"],
            config["db-username"],
            config["db-password"],
            config["db-database"],
            sql,
            data_number,
        )
        for item in data:
            tmp = {}
            for idx, col in enumerate(cols):
                if col in fields:
                    tmp[col] = item[idx]
            if tmp:
                results.append(tmp)
        if results:
            tables.append({"data": results, "table_name": table_name})
    return tables


def package_tables_data(tables: list) -> dict:
    """
    将从数据库中提取到的数据打包为展示数据
    Args:
        tables:

    Returns:

    """
    for table in tables:
        df = pd.DataFrame(table["data"])
        table["html"] = df.T.to_html(classes=["table", "extracted-table-data"])
    return {"table_numbers": len(tables), "tables": tables}


def extract_data_from_json(data):
    """
    从json文件中提取
    Args:
        data:

    Returns:

    """
    result = []
    for foo in data:
        model_type = foo.pop("EntType")
        mod = getattr(
            importlib.import_module("application.models", model_type), model_type
        )
        if mod:
            tmp = mod()
            result.append(tmp.extract_json(foo))
    return unique_list_dict_via_one_key("s_name", result)


def extract_data_from_json_file_v1(files: MultiDict):
    """
    提取json文件中的数据,将所有文件中的数据解析,并将其中的标准数据合并为一个大的字典
    Args:
        files:

    Returns:

    """
    result = {}
    for _, file in files.items():
        file_content = json.load(file)
        if isinstance(file_content, dict):
            parser_json_file_v1(file_content, result)
        else:
            raise Exception("error data type")
    return result


def extract_data_from_different_type_file(file):
    """
    从不同的文件类型中获取数据
    Returns:

    """
    if (
            file.mimetype == "application/vnd.openxmlformats-"
                             "officedocument.spreadsheetml.sheet"
    ):
        return extract_data_from_excel_file(file)
    elif file.mimetype == "text/csv":
        return extract_data_from_csv_file(file)
    elif file.mimetype == "text/plain":
        return extract_data_from_text_file(file)
    elif file.mimetype == "application/json":
        return extract_data_from_json_file(file)
    else:
        raise Exception("unknown file type")


def package_tables_data_v2(tables: list) -> list:
    """

    Args:
        tables:

    Returns:

    """
    result = []
    for table in tables:
        cols = table["data"][0].keys()
        tmp = {
            "columns": [{"title": col, "dataIndex": col} for col in cols],
            "data": table["data"],
            "table_name": table["table_name"],
        }
        result.append(tmp)

    return result


def task_returner(task) -> dict:
    """
    根据不同的task状态生成不同的返回值
    Args:
        task:

    Returns:

    """
    if task.state == "PENDING":
        response = {
            "state": "empty task",
            "info": {"current": 0, "total": 4, "status": "empty task"},
        }
    elif task.state == "FILL DATA":
        response = {
            "state": task.state,
            "info": task.info,
        }
    elif task.state == "SUCCESS":
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
    return response


def build_sandbox_from_structure_data(data, current_user):
    """
    从结构化数据中构建sandbox
    Args:
        current_user:
        data:

    Returns:

    """
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
    return task
