# -*- coding: utf-8 -*-
"""
    :time: 2021/3/8 17:31
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: docker_handler.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import docker

from config.settings import DOCKER_NEO4J_IMAGES_VERSION


def get_all_container_and_classify() -> dict:
    """
    获取所有的container并且分类
    Returns:
        {
            'running':[],
            'exited':[],
        }
    """
    res = {"running": [], "exited": []}
    client = docker.from_env()
    containers = client.containers.list(all=True)
    for container in containers:
        container_tag = container.image.tags[0]
        if container_tag in DOCKER_NEO4J_IMAGES_VERSION:
            if container.status == "running":
                res["running"].append(container)
            elif container.status == "exited":
                res["exited"].append(container)
            else:
                pass
    return res
