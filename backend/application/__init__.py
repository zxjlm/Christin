"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: __init__.py.py
@time: 2020/12/26 13:46
@desc:
"""
import os

import flask_wtf
from flask import Flask, request
from flask_security import SQLAlchemyUserDatastore

from application.views import all_bp
from application.extensions import db, migrate, security, babel, swagger

# import application.models
from config import import_config
from config.settings import LANGUAGES


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")

    app = Flask("application")

    if config_name == "test":
        app.env = "test"
    config = import_config(app.env)
    app.config.from_object(config)  # 加载配置模块

    register_extensions(app)
    register_blueprints(app)
    register_api_code(app)
    # register_commands(app)
    # register_errors(app)
    # register_template_context(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app)
    swagger.init_app(app)
    flask_wtf.CSRFProtect(app)
    # Setup Flask-Security
    from application.models.authbase import User, Role

    # from application.forms.user import ExtendedLoginForm

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(
        app,
        datastore=user_datastore,
        # login_form=ExtendedLoginForm,
        # register_form=ExtendedRegisterForm
    )


def register_blueprints(app):
    for bp in all_bp:
        app.register_blueprint(bp)


def register_api_code(app):
    from application.extensions import apicode

    apicode.init_app(app.config)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())
