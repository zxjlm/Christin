"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: user.py
@time: 2021/1/24 16:20
@desc:
"""
from flask_babel import lazy_gettext
from flask_security import RegisterForm, LoginForm
from flask_security.forms import password_required, email_required
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from application.models.authbase import User


class BootstrapFromStringField(StringField):
    pass


class UserForm(User):
    username = StringField(lazy_gettext("Username"))


class ExtendedLoginForm(LoginForm):
    email = EmailField(lazy_gettext("Email Address"), validators=[email_required])
    password = PasswordField(lazy_gettext("Password"), validators=[password_required])
    remember = BooleanField(lazy_gettext("Remember Me"))
    submit = SubmitField(lazy_gettext("Login"))


class ExtendedRegisterForm(RegisterForm):
    sex = StringField("Sex", [DataRequired()])
    age = StringField("Age", [DataRequired()])
    name = StringField("Name", [DataRequired()])
