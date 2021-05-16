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
    # __tablename__ = 'tb_sy_role'
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # dt_create_date_time = db.Column(db.DateTime, index=True,
    #                                 default=datetime.now)
    # dt_update_datetime = db.Column(db.DateTime, index=True,
    #                                default=datetime.now)
    # s_name = db.Column(db.String(100))
    # s_description = db.Column(db.String(200))
    # s_icon_cls = db.Column(db.String(100))
    # i_seq = db.Column(db.Integer)
    #
    # # 包含资源
    # resources = db.relationship('Resource',
    #                             secondary=role_resource_table,
    #                             backref=db.backref('roles',
    #                                                lazy='dynamic'))  # 资源所属角色

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

    # def __repr__(self):
    #     return "<Role name:%r description:%r iconCls:%r seq:%r>\n" % (
    #         self.s_name,
    #         self.s_description,
    #         self.s_icon_cls,
    #         self.i_seq,
    #     )

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
