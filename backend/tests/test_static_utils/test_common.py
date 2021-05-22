# -*- coding: utf-8 -*-
"""
    :time: 2021/3/8 16:45
    :author: Harumonia
    :url: http://harumonia.moe
    :project: Christin
    :file: test_common.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from application.controllers.main_apis_controllers import package_data_for_sandbox
from application.utils.data_management_reducer import get_cls_primary_key


def test_key_map():
    assert get_cls_primary_key("Herb") == "bin_hid"
    assert get_cls_primary_key("Prescription") == "bin_pid"


def test_sandbox_data_package():
    data_list = [
        {
            "text": "矮地茶,艾叶,安息香",
            "ents": [[0, 3, "HERB"], [4, 6, "HERB"], [7, 10, "HERB"]],
            "links": [{"rel_name": "Test", "left": "矮地茶", "right": "安息香"}],
        }
    ]
    res_dict = {
        "nodes": [
            {"name": "矮地茶", "type": "HERB"},
            {"name": "艾叶", "type": "HERB"},
            {"name": "安息香", "type": "HERB"},
        ],
        "relationships": [{"rel_name": "Test", "left": "矮地茶", "right": "安息香"}],
    }
    assert package_data_for_sandbox(data_list) == res_dict
