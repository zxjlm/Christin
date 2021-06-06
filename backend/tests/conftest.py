"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: conftest.py
@time: 2021/1/12 9:11 下午
@desc:
"""
import json

import pytest

from application import create_app, db
from application.models import User, Labels, Role


@pytest.fixture
def client():
    app = create_app('test')

    # app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            role1 = Role(name='admin', description='管理员')
            role2 = Role(name='user', description='用户')
            db.session.add(role1)
            db.session.add(role2)
            user1 = User(name='zxj', sex='M', email='test@me.com', password='test', active=True,
                         fs_uniquifier='e67fa8573c2d42198aeed56d019a2032')
            user2 = User(name='normal_user', sex='M', email='user@me.com', password='test', active=True,
                         fs_uniquifier='e67fa8573c2d42198aeed56d019a2031')
            user1.roles = [role1]
            user2.roles = [role2]
            db.session.add(user1)
            db.session.add(user2)
            label1 = Labels(s_label='ZZ', s_name='ZZ')
            label2 = Labels(s_label='CD', s_name='CD')
            db.session.add(label1)
            db.session.add(label2)
            db.session.commit()

            yield client


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, email="test@me.com", password="test"):
        return self._client.post(
            "/api/accounts/login",
            data=json.dumps({'email': email, 'password': password}),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        )

    def logout(self):
        return self._client.get(
            "/api/accounts/logout",
            headers={
                'Accept': 'application/json',
            })


@pytest.fixture
def auth(client):
    return AuthActions(client)
