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
        # Flask 3 removed app.env / FLASK_ENV. Keep the Flask 2 default of
        # "production" when neither override is set so Docker/Gunicorn
        # deployments stay on ProductionConfig.
        config_name = os.getenv("FLASK_CONFIG") or os.getenv("FLASK_ENV", "production")

    app = Flask("application")
    config = import_config(config_name)
    app.config.from_object(config)  # 加载配置模块
    # Flask 3 reads these from the JSON provider, not JSON_AS_ASCII / JSON_SORT_KEYS.
    app.json.ensure_ascii = False
    app.json.sort_keys = False

    register_extensions(app)
    register_blueprints(app)
    register_api_code(app)
    # register_commands(app)
    # register_errors(app)
    # register_template_context(app)
    return app


def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app, locale_selector=get_locale)
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
