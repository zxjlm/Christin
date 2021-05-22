# -*- coding:utf-8 -*-
import datetime
import time

from sqlalchemy import Column, SmallInteger, DateTime, Integer

__author__ = "harumonia"

from application.extensions import db
from sqlalchemy.sql import func


class BaseModel(db.Model):
    """
    为药材和处方而服务的第一基类
    """

    __abstract__ = True

    i_status = Column(SmallInteger, default=1, comment="状态码")
    dt_create_datetime = Column(
        DateTime, nullable=False, server_default=func.now(), comment="数据生成的日期"
    )
    dt_update_datetime = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=datetime.datetime.utcnow,
        comment="数据最终修改的日期",
    )
    i_user_id = Column(db.String(36), comment="创建人id(备用字段)", default="")
    s_mark = Column(db.String(500), comment="备注", default="")

    def add(self, data):
        data["i_status"] = 1
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key) and key != "bin_hid":
                setattr(self, key, value)
        db.session.add(self)
        db.session.commit()

    def fake_delete(self):
        self.update({"i_status": 0})
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def lock_field():
        return [
            "i_status",
            "dt_create_datetime",
            "dt_update_datetime",
            "i_user_id",
            "bin_id",
        ]

    @staticmethod
    def lock_field_output():
        return ["dt_create_datetime", "dt_update_datetime", "i_status"]

    @staticmethod
    def data_table_fields() -> list:
        """
        数据表的字段列表
        Returns:

        """
        return ["id", "s_name"]

    def to_dict(self):
        res = {}
        for attribute in self.__dict__.keys():
            if attribute[:1] != "_" and attribute not in self.lock_field_output():
                value = getattr(self, attribute)
                if not callable(value):
                    res[attribute] = value
        return res
