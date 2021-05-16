# -*- coding: utf-8 -*-
"""
    :time: 2021/3/8 17:54
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: dashboard_main.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from application.utils.docker_handler import get_all_container_and_classify
from application.models.authbase.logs import AnalysesLog


def docker_neo4j_list():
    res = []
    neo_dict = get_all_container_and_classify()
    for status, neo_containers in neo_dict.items():
        for neo_container in neo_containers:
            item = AnalysesLog.query.filter_by(s_mark=neo_container.name).first()
            if item:
                item = item.to_dict()
                if item["status"] != "creating":
                    item["status"] = status
            else:
                item = {
                    "create_date_time": "",
                    "update_date_time": "",
                    "login_name": "",
                    "s_project_name": "undefined project",
                    "status": status,
                    "mark": neo_container.name,
                }
            res.append(item)
    return res
