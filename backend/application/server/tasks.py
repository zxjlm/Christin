# -*- coding: utf-8 -*-
"""
    :time: 2021/1/20 17:54
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: tasks.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import os
import time
from functools import reduce

import docker
import redis
from celery import Celery
from flask_mail import Message
from loguru import logger
from py2neo import Graph

from application.utils.mysql_handler import change_project_status, update_task_process
from application.utils.neo4j_handler import (
    get_remote_graph_from_one_node,
    get_neo4j_version,
    get_neo_file_path,
)
from application.utils.normal import generate_password, send_mail, generate_mail_html
from application.utils.port_scanner import PortDetect
from config.secure import SecureInfo
from config.settings import NEO_HOST, REDIS_HOST, SERVER

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 5)
    return True


@celery.task(bind=True)
def long_task(
    self, data_list: dict, project_name: str, need_email: str, email_address: str
):
    """

    Args:
        email_address: 邮件地址
        need_email: 需要发送邮件
        project_name: 项目名称
        self:
        data_list: {
            nodes:[]
            relationships:[]
        }

    Returns:

    """
    t1 = time.time()

    port = PortDetect(7777, 7800).get_available_range()
    pwd = generate_password()
    id_ = self.request.id

    # 在js取到 data['state'] != 'CREATE NEO4J SANDBOX' 后将配置展示(仅仅展示)
    self.update_state(
        state="CREATE NEO4J SANDBOX",
        meta={"current": 1, "total": 4, "status": "", "port": port, "password": pwd},
    )
    update_task_process(id_, 1)

    container = None
    try:
        client = docker.from_env()
        container = client.containers.run(
            get_neo4j_version(),
            detach=True,
            environment=[f"NEO4J_AUTH=neo4j/{pwd}"],
            volumes={get_neo_file_path() + id_: {"bind": "/data", "mode": "rw"}},
            # remove=True,
            ports={"7687/tcp": port},
            name=id_,
        )
        config = {
            "container_id": container.id,
            "port": port,
            "password": pwd,
            "task_id": id_,
        }

        self.update_state(
            state="INITIALIZE NEO4J", meta={"current": 2, "total": 4, "status": ""}
        )
        update_task_process(id_, 2)
    except Exception as _e:
        if container and container.status != "exited":
            container.stop()
            container.remove()
        change_project_status(id_, status=0)
        raise Exception(_e)

    # 等待sandbox中的neo4j完成启动
    connect_failed_times = 0
    while connect_failed_times <= 4:
        time.sleep(15)
        try:
            Graph("bolt://{}:{}".format(NEO_HOST, str(port)), password=pwd)
            break
        except Exception as _e:
            logger.warning(
                f"{id_} connect failed, "
                f"retry {connect_failed_times},"
                f" error is {_e}"
            )
            connect_failed_times += 1
            continue

    if connect_failed_times > 4:
        if container and container.status != "exited":
            container.stop()
            container.remove()
        change_project_status(id_, status=0)
        raise Exception("time over")

    self.update_state(state="FILL DATA", meta={"current": 3, "total": 4})
    update_task_process(id_, 3)
    # 生成子图
    try:
        base_graph = Graph(
            "bolt://" + NEO_HOST + ":" + SecureInfo.get_neo4j_port(),
            password=SecureInfo.get_neo4j_password(),
        )
        new_graph = Graph("bolt://" + NEO_HOST + ":" + str(port), password=pwd)

        nodes = data_list["nodes"]
        # 关系暂时不考虑
        # relationships = data_list['relationships']
        subgraph_list = []

        # r = redis.Redis(host=REDIS_HOST, port=6379, db=1)

        for node in nodes:
            subgraph = get_remote_graph_from_one_node(base_graph, node)
            if subgraph:
                # r.lpush(f"{id_}-midway-success", node["name"])
                subgraph_list.append(subgraph)
            # else:
            # r.lpush(f"{id_}-midway-failed", node["name"])

        if len(subgraph_list) > 1:
            subgraph_fin = reduce(lambda x, y: x | y, subgraph_list)
            new_graph.create(subgraph_fin)
        elif len(subgraph_list) == 1:
            subgraph_fin = subgraph_list[0]
            new_graph.create(subgraph_fin)
        else:
            pass
    except Exception as _e:
        logger.error(f"{id_} failed, {container.status}")
        logger.exception(_e)
        if container and container.status != "exited":
            container.stop()
            container.remove()
        change_project_status(id_, status=0)
        raise Exception(_e)

    # self.update_state(state='COMPLETE',
    #                   meta={'current': 4, 'total': 4})

    runtime = round(time.time() - t1, 4)
    change_project_status(id_, config, runtime)

    if need_email:
        html = generate_mail_html(pwd, port, SERVER, runtime)
        send_mail(
            subject=f"neo create success, project: {project_name}",
            receivers=[email_address],
            html=html,
        )

    time.sleep(2)
    update_task_process(id_, 4)
    # 可以在return时加上密码和端口，供用户自己连接neo4j
    return {"current": 4, "total": 4, "config": config, "status": "Task completed!"}


@celery.task(bind=True)
def long_task_for_test(
    self, data_list: dict, project_name: str, need_email: str, email_address: str
):
    """
    测试用的task
    Args:
        email_address:
        need_email:
        project_name:
        self:
        data_list:

    Returns:

    """
    port = 7687
    pwd = "zxjzxj233"
    id_ = self.request.id

    t1 = time.time()

    # 在js取到 data['state'] != 'CREATE NEO4J SANDBOX' 后将配置展示(仅仅展示)
    self.update_state(
        state="CREATE NEO4J SANDBOX",
        meta={"current": 1, "total": 4, "status": "", "port": port, "password": pwd},
    )

    client = docker.from_env()
    container = client.containers.run("redis", detach=True, name=id_)

    config = {
        "container_id": container.id,
        "port": port,
        "password": pwd,
        "task_id": id_,
    }

    r = redis.Redis(host=REDIS_HOST, port=6379, db=1)
    r.lpush(f"{id_}-midway-success", "test-success")
    r.lpush(f"{id_}-midway-failed", "test-failed")

    time.sleep(3)

    self.update_state(
        state="INITIALIZE NEO4J", meta={"current": 2, "total": 4, "status": ""}
    )
    time.sleep(3)

    self.update_state(state="FILL DATA", meta={"current": 3, "total": 4})

    r.set("11", "22")
    for foo in ["aaa", "bbb", "ccc"]:
        if foo == "aaa":
            r.lpush(f"{id_}-midway-success", foo)
        else:
            r.lpush(f"{id_}-midway-failed", foo)
        time.sleep(2)

    runtime = round(time.time() - t1, 4)
    change_project_status(id_, config, runtime)

    if need_email:
        html = generate_mail_html(pwd, port, SERVER, runtime)
        send_mail(
            subject=f"neo create success, project: {project_name}",
            receivers=[email_address],
            html=html,
        )

    # 可以在return时加上密码和端口，供用户自己连接neo4j
    return {"current": 4, "total": 4, "config": config, "status": "Task completed!"}


@celery.task
def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(
        email_data["subject"],
        sender=celery.config["MAIL_DEFAULT_SENDER"],
        recipients=[email_data["to"]],
    )
    msg.body = email_data["body"]


@celery.task(bind=True)
def neo_start(self, container_name, project_name, port, pwd):
    """
    启动neo4j
    Args:
        pwd:
        port:
        project_name:
        self:
        container_name:

    Returns:

    """
    # 在js取到 data['state'] != 'CREATE NEO4J SANDBOX' 后将配置展示(仅仅展示)
    self.update_state(
        state="START NEO4J SANDBOX", meta={"current": 1, "total": 2, "status": ""}
    )

    client = docker.from_env()
    container = client.containers.get(container_name)
    container.start()

    connect_failed_times = 0
    while connect_failed_times <= 4:
        time.sleep(10)
        try:
            Graph("bolt://{}:{}".format(NEO_HOST, str(port)), password=pwd)
            break
        except Exception as _e:
            logger.info(f"neo4j initializing, {_e}")
            connect_failed_times += 1
            continue

    if connect_failed_times > 4:
        raise Exception("time over")

    change_project_status(container_name)
    send_mail(subject=f"neo create success, project: {project_name}")

    return {"current": 2, "total": 2, "status": "Task completed!"}
