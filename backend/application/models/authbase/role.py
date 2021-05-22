# coding:utf-8

from flask_security.models import fsqla_v2 as fsqla

from application.extensions import db

role_resource_table = db.Table(
    "tb_rel_role_resource",
    db.metadata,
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    db.Column("resource_id", db.String(36), db.ForeignKey("resource.id")),
)


class Role(db.Model, fsqla.FsRoleMixin):

    def resources_update(self):
        # db.session.add()
        # self.id
        pass

    def get_id(self):
        return str(self.id)

    def to_dict_simple(self):
        return dict(
            [
                (k, getattr(self, k))
                for k in self.__dict__.keys()
                if not k.startswith("_")
            ]
        )

    @staticmethod
    def data_table_fields() -> list:
        """
        数据表的字段列表
        Returns:

        """
        return ["id", "update_datetime", "s_name", "description"]

    def to_dict(self):
        return {
            "id": self.id,
            "update_datetime": self.update_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "s_name": self.name,
            "description": self.description,
        }
