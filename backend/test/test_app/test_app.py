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
import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# def login(client, username, password):
#     return client.post(
#         "/login",
#         data=dict(username=username, password=password),
#         follow_redirects=True,
#     )
#
#
# def logout(client):
#     """Logout helper function"""
#     return client.get("/logout", follow_redirects=True)
#
#
# def test_login_logout(client):
#     """Test login and logout using helper functions"""
#     rv = login(client, app.config["USERNAME"], app.config["PASSWORD"])
#     assert b"You were logged in" in rv.data
#     rv = logout(client)
#     assert b"You were logged out" in rv.data
#     rv = login(client, app.config["USERNAME"] + "x", app.config["PASSWORD"])
#     assert b"Invalid username" in rv.data
#     rv = login(client, app.config["USERNAME"], app.config["PASSWORD"] + "x")
#     assert b"Invalid password" in rv.data


def test_home(client):
    response = client.get("/")

    assert response.status_code == 302


# def test_spacy(client):
#     import json
#     response = client.post('/my_model', json={
#         'message': '近一周饮食不当,一度腹泻,日3次,泻下后精神疲烦,时有低热,'
#                    '怕风,口干,痰中夹有血丝,左侧胸痛时作'})
#     resp_json = json.loads(response.data)
#     assert response.status_code == 200
#     assert resp_json['code'] == 200
#     assert len(resp_json['data']) > 0
