from flask_login import UserMixin
from datetime import datetime

from application.extensions import db


class ResourceType(db.Model, UserMixin):
    __tablename__ = "resource_type"
    id = db.Column(db.String(36), primary_key=True)
    dt_create_date_time = db.Column(db.DateTime, index=True, default=datetime.now)
    dt_update_datetime = db.Column(db.DateTime, index=True, default=datetime.now)
    s_name = db.Column(db.String(100))
    s_description = db.Column(db.String(200))

    resources = db.relationship("Resource", backref="type", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "create_datetime": self.dt_create_date_time,
            "update_datetime": self.dt_update_datetime,
            "name": self.s_name,
            "description": self.s_description,
        }

    def __repr__(self):
        return "<ResourceType %r>\n" % self.s_name
