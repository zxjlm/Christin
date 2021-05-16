# -*- coding: utf-8 -*-
"""
    :time: 2021/1/28 15:12
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: neo4j_handler.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import sys
from functools import reduce
from typing import Union

from loguru import logger
from py2neo import Node, Relationship, Graph, Subgraph, NodeMatcher

from application.utils.custom_exceptions import Neo4jUpdateFailedException


def get_neo4j_version():
    """
    针对不同的平台获取不同的neo4j版本
    Returns:

    """
    if sys.platform == "darwin":
        return "c034d2c34558"
    else:
        return "neo4j:3.5.12"


def get_neo_file_path():
    """
    针对不同平台获取不同的卷组路径
    Returns:

    """
    if sys.platform == "darwin":
        return "/Users/zhangxinjian/docker-data/neo-data"
    else:
        return "/root/neo4j-data/"


def get_remote_graph_from_one_node(
    base_graph: Graph, node: dict
) -> Union[Subgraph, None]:
    """

    Args:
        base_graph:
        node: 新数据集包含的node {'type':'','name':''}

    Returns:

    """
    type_ = node["type"][0] + node["type"][1:].lower()
    type_valid = ["Herb", "Disease", "Gene", "MM_symptom", "Mol", "TCM_symptom"]
    if type_ not in type_valid:
        logger.warning("{} type not valid".format(node))
        return Node(type_, s_name=node["name"])

    cypher = (
        f"MATCH p=(n:{type_})-[]->()-[]->() WHERE n.s_name='"
        f"{node['name']}' RETURN DISTINCT p"
    )
    query_res = base_graph.run(cypher)

    query_subgraph = query_res.to_subgraph()
    if not query_subgraph:
        logger.warning("{} not find graph".format(node))
        if "s_name" in node:
            return Node(type_, **node)
        else:
            sname = node.pop("name")
            return Node(type_, s_name=sname, **node)

    nods = list(query_subgraph.nodes)
    rels = list(query_subgraph.relationships)

    new_nodes = {node.identity: Node(str(node.labels)[1:], **node) for node in nods}

    result = []
    for rel in rels:
        type_ = list(rel.types())[0]
        ty = Relationship.type(type_)
        lab1 = rel.start_node.identity
        lab2 = rel.end_node.identity
        result.append(ty(new_nodes[lab1], new_nodes[lab2]))
    subgraph = reduce(lambda x, y: x | y, result)
    logger.info("{} generate success".format(node))
    return subgraph


def neo_data_update_trigger(type_: str, data: dict):
    """
    在更新数据库的同时触发该函数，同步更新本源neo库
    Args:
        type_:
        data: 该数据或许需要经过一轮处理

    Returns:

    """
    try:
        # cypher = "MATCH a=({s_name:'{}'}) return a".format(data['s_name'])
        graph = Graph("bolt://39.99.178.69:7687", password="zxjzxj233")
        node_match = NodeMatcher(graph)
        node_iter = node_match.match(type_, s_name=data["s_name"])
        node = list(node_iter)
        if len(node) == 1:
            node = node[0]
            node.update(**data)
            graph.push(node)
            return True
        else:
            return "failed, many data were queried"
    except Exception as _e:
        raise Neo4jUpdateFailedException(_e)


def neo_data_create_trigger(type_: str, data: dict):
    """
    在数据库添加数据的同时触发该函数，同步更新本源neo库
    Args:
        type_:
        data: 该数据或许需要经过一轮处理

    Returns:

    """
    try:
        # cypher = "MATCH a=({s_name:'{}'}) return a".format(data['s_name'])
        graph = Graph("bolt://39.99.178.69:7687", password="zxjzxj233")
        node = Node(type_, **data)
        graph.create(node)
        return True
    except Exception as _e:
        logger.error(f"failed when update neo4j, {data}, {_e}")
        return "failed, manually check"
