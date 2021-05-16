from flask_login import UserMixin
from datetime import datetime

from application.extensions import db


class Resource(db.Model, UserMixin):
    __tablename__ = "resource"
    id = db.Column(db.String(36), primary_key=True)
    dt_create_date_time = db.Column(db.DateTime, index=True, default=datetime.now)
    dt_update_datetime = db.Column(db.DateTime, index=True, default=datetime.now)
    s_name = db.Column(db.String(100))
    s_url = db.Column(db.String(200))
    s_description = db.Column(db.String(200))
    s_icon_cls = db.Column(db.String(100))
    i_seq = db.Column(db.Integer)
    s_target = db.Column(db.String(100))

    s_sy_resource_type_id = db.Column(db.String(36), db.ForeignKey("resource_type.id"))

    s_sy_resource_id = db.Column(db.String(36), db.ForeignKey("resource.id"))

    parent = db.relationship(
        "Resource", remote_side=[id], backref="resource", uselist=False
    )

    def get_id(self):
        return str(self.id)

    def to_dict(self):
        return {
            "id": self.id,
            "create_datetime": self.dt_create_date_time,
            "update_datetime": self.dt_update_datetime,
            "name": self.s_name,
            "url": self.s_url,
            "description": self.s_description,
            "iconCls": self.s_icon_cls,
            "seq": self.i_seq,
            "target": self.s_target,
            "pid": self.get_pid(),
            "sy_resource_type": self.get_type_json(),
        }

    def to_menu_json(self):
        return {
            "id": self.id,
            "iconCls": self.s_icon_cls,
            "pid": self.get_pid(),
            "state": "open",
            "checked": False,
            "attributes": {"target": self.s_target, "url": self.s_url},
            "text": self.s_name,
            "seq": self.i_seq,
        }

    def get_pid(self):
        if self.parent:
            return self.parent.id
        return ""

    def get_type_json(self):
        if self.type:
            return self.type.to_dict()
        return {}

    def __repr__(self):
        return "<Resource name:%r url:%r>\n" % (self.s_name, self.s_url)
