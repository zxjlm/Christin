"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: test_app.py
@time: 2021/1/16 8:38 上午
@desc:
"""

import json


def login(client, username, password, type_='json'):
    post_data = {'email': username, 'password': password}
    if type_ == 'json':
        return client.post(
            "/api/accounts/login",
            data=json.dumps(post_data),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            follow_redirects=True,
        )
    else:
        return client.post(
            "/api/accounts/login",
            data=post_data,
            follow_redirects=True
        )


def logout(client):
    return client.get("/api/accounts/logout")


def test_login_page(client):
    """
    测试登录页面
    Args:
        client:

    Returns:

    """
    rv = login(client, 'test', 'test', 'html')
    assert 'dashlite' in rv.data.decode()


def test_login_logout(client):
    """
    测试登录/登出/及其产生的冲突
    Args:
        client:

    Returns:

    """
    rv = login(client, 'test@me.com', 'test')
    assert rv.status_code == 200 and rv.json['meta']['code'] == 200
    # 重复登录
    rv = login(client, 'test@me.com', 'test')
    assert rv.json['response']['error'] == 'You can only access this endpoint when not logged in.'
    # 登出
    rv = logout(client)
    assert rv.status_code == 302


def test_home(client):
    response = client.get("/")
    assert response.status_code == 302


def test_authorization(client):
    """
    测试 - 登录访问权限
    Args:
        client:

    Returns:

    """
    rv = client.get('/main/api/v2/currentUser')
    assert rv.status_code == 302


def test_get_current_user_info(client, auth):
    """
    测试 - 获取当前用户信息
    Args:
        client:

    Returns:

    """
    auth.login()
    rv = client.get('/main/api/v2/currentUser')
    assert rv.json['s_name'] == 'zxj'


def test_get_project_runtime(client, auth):
    """
    测试 - 获取项目运行状态信息
    Args:
        client:

    Returns:

    """
    auth.login()
    rv = client.get('/main/api/v2/currentUser')
    assert rv.json['s_name'] == 'zxj'

# def test_spacy(client):
#     import json
#     response = client.post('/my_model', json={
#         'message': '近一周饮食不当,一度腹泻,日3次,泻下后精神疲烦,时有低热,'
#                    '怕风,口干,痰中夹有血丝,左侧胸痛时作'})
#     resp_json = json.loads(response.data)
#     assert response.status_code == 200
#     assert resp_json['code'] == 200
#     assert len(resp_json['data']) > 0
