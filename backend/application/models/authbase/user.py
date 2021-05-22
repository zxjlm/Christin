from flask_security.models import fsqla_v2 as fsqla

from application.extensions import db


class User(db.Model, fsqla.FsUserMixin):
    # __tablename__ = 'tb_sy_user'
    name = db.Column(db.String(100))
    sex = db.Column(db.String(1))
    age = db.Column(db.Integer)

    logs = db.relationship("AnalysesLog", backref=db.backref("user"))

    @staticmethod
    def data_table_fields() -> list:
        """
        数据表的字段列表
        Returns:

        """
        return ["id", "username", "s_name", "last_login_date"]

    def to_dict(self):
        return {
            "id": self.id,
            "s_name": self.name,
            "username": self.username,
            "last_login_date": self.last_login_at,
        }
