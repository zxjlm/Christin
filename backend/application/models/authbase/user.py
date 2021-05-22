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

    # def get_id(self):
    #     return str(self.id)

    # def have_permission(self, url):
    #     permissions = []
    #     for role in self.roles:
    #         permissions.extend([resource for resource in role.resources])
    #
    #     if filter(lambda x: x.s_url == url, permissions):
    #         return True
    #
    #     permissions = []
    #     for organization in self.organizations:
    #         permissions.extend(
    #             [resource for resource in organization.resources])
    #
    #     return filter(lambda x: x.s_name == url, permissions)

    # def __repr__(self):
    #     return '<User %r>\n' % self.s_name
    #
    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'create_datetime': self.dt_create_date_time.strftime(
    #             '%Y-%m-%d %H:%M:%S'),
    #         'update_datetime': self.dt_update_datetime.strftime(
    #             '%Y-%m-%d %H:%M:%S'),
    #         'login_name': self.s_login_name,
    #         'name': self.s_name,
    #         'sex': self.s_sex,
    #         'age': self.i_age,
    #         'photo': self.s_photo,
    #         # 'employdate': self.s_employ_date.strftime('%Y-%m-%d %H:%M:%S'),
    #     }
    #
    # def get_authority_list(self):
    #     role = self.roles[0]
    #     authority_list = role.resources
    #     res = [{'name': foo.s_name, 'url': foo.s_url, 'attr': foo.s_description}
    #            for
    #            foo in authority_list]
    #     return res

    # def update_last_login_time(self, ip):
    #     self.dt_update_datetime = datetime_creator()
    #     online = online()
    #     online.s_sy_user_id = self.id
    #     online.dt_create_date_time = self.dt_update_datetime
    #     online.IP = ip
    #     online.s_login_name = self.s_login_name
    #     online.TYPE = '1'
    #     db.session.add(self)
    #     db.session.add(online)
    #     db.session.commit()

    # def add_data(self, data):
    #     for key, value in data.items():
    #         if hasattr(self, key):
    #             setattr(self, key, value)
    #     db.session.add(self)
    #     db.session.commit()
