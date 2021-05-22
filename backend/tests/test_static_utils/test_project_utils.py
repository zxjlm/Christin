"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: test_project_utils.py
@time: 2021/5/22 8:20 下午
@desc:
"""
from application.controllers.main_apis_controllers import package_data_for_sandbox
from application.models import Herb
from application.utils.data_management_reducer import get_cls_primary_key, is_locked_field_in, check_model_name


def test_sql_checkers():
    """
    测试数据库的各个约束函数
    Returns:

    """
    assert get_cls_primary_key("Herb") == "bin_hid"
    assert get_cls_primary_key("Prescription") == "bin_pid"

    assert ~is_locked_field_in({'i_status': 1}, Herb)

    assert check_model_name('Herb')


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
