# -*- coding: utf-8 -*-
"""
    :author: Harumonia
    :url: http://harumonia.top
    :copyright: © 2020 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
# from flask_login import LoginManager
from flasgger import Swagger
from flask_babel import Babel
from flask_migrate import Migrate
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy

from config.apiconfig import ApiCode
from flask_security.models import fsqla_v2 as fsqla

apicode = ApiCode()

db = SQLAlchemy()
migrate = Migrate()
babel = Babel(default_locale="zh")
fsqla.FsModels.set_db_info(db)
# login_manager = LoginManager()
# login_manager.session_protection = 'Wp0J24oSeOkWBoMzJc'
security = Security()
swagger = Swagger()
