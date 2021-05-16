import json

from sqlalchemy import ForeignKey

from application.extensions import db

from application.models.base import BaseModel


class AnalysesLog(BaseModel):
    __tablename__ = "analyses_log"
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    s_sy_user_id = db.Column(db.Integer, ForeignKey("user.id"))
    s_file_name = db.Column(db.String(100), default="")
    i_rows_number = db.Column(db.INT, default=0)
    j_data = db.Column(db.JSON, default="", comment="记录分析的数据")
    j_remark = db.Column(db.JSON, default="", comment="记录各种参数")
    j_result = db.Column(db.JSON, default="", comment="记录结果")
    s_project_name = db.Column(
        db.String(50), nullable=False, comment="项目名", default="unnamed"
    )
    s_project_description = db.Column(db.String(1000), comment="项目描述", default="")
    f_runtime = db.Column(db.FLOAT, default=-1.0, comment="运行时间")
    i_analysis_type = db.Column(db.SmallInteger, comment="结构化类型")

    i_current_step = db.Column(db.SmallInteger, default=0, comment="目前的进度")
    i_total_step = db.Column(db.SmallInteger, default=4, comment="总进度")

    fk_user = db.relationship("User", backref=db.backref("fk_analyse_log"))

    def __repr__(self):
        return "<s_sy_user_id %r , filename %r>\n" % (self.s_login_name, self.file_name)

    def to_dict(self):
        return {
            "create_date_time": self.dt_create_datetime,
            "update_date_time": self.dt_update_datetime,
            "s_project_description": self.s_project_description,
            "login_name": self.fk_user.email,
            "s_project_name": self.s_project_name,
            "status": self.get_mapper()[self.i_status],
            "mark": self.s_mark,
            "analyse_type": self.i_analysis_type,
            "current_step": self.i_current_step,
            "total_step": self.i_total_step,
        }

    def to_dict_particular(self):
        return {
            "create_date_time": self.dt_create_datetime,
            "update_date_time": self.dt_update_datetime,
            "login_name": self.fk_user.email,
            "s_project_description": self.s_project_description,
            "s_project_name": self.s_project_name,
            "status": self.get_mapper()[self.i_status],
            "mark": self.s_mark,
            "runtime": self.f_runtime,
            "data": self.j_data,
            "remark": self.j_remark,
            "analyse_type": self.i_analysis_type,
            "current_step": self.i_current_step,
            "total_step": self.i_total_step,
        }

    @staticmethod
    def get_mapper():
        """
        项目状态映射表
        Returns:

        """
        return ["deleted", "running", "exited", "creating"]

    def add(self, data):
        data["i_status"] = 3
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.fk_user = data["current_user"]
        self.j_data = json.dumps(data["data"], ensure_ascii=False)

        db.session.add(self)
        db.session.commit()

    def stop(self):
        self.update({"i_status": 2})
        db.session.add(self)
        db.session.commit()

    # def add(self, loginname, usrid, file_name, rows_number, date, data=""):
    #     self.file_name = file_name
    #     self.rows_number = rows_number
    #     self.s_login_name = loginname
    #     self.s_sy_user_id = usrid
    #     self.dt_create_date_time = date
    #     # self.type = type
    #     self.data = data
    #
    #     db.session.add(self)
    #     db.session.commit()
    #
    # def dele(self):
    #     db.session.delete(self)
    #     db.session.commit()


# class AnalysesResLog(BaseModel):
#     __tablename__ = 'analyses_res_log'
#     id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
#     dt_create_date_time = db.Column(db.DateTime, index=True,
#                                     default=datetime.now)
#     s_sy_user_id = db.Column(db.Integer, ForeignKey('user.id'))
#     js_data = db.Column(db.JSON, default="", comment="结果数据")
#     s_options = db.Column(db.String(100), comment="参数选择")
#     s_analyse_type = db.Column(db.String(30), comment="分析类型")
#     s_test_columns = db.Column(db.String(30), comment="测试冗余列")
#
#     def export(self):
#         import pandas as pd
#         df = pd.read_json(self.data)
#         df.to_csv(
#             "{}_{}.csv".format(self.s_sy_user_id, self.dt_create_date_time))
#         print("{}_{}.csv   export over".format(self.s_sy_user_id,
#                                                self.dt_create_date_time))

# def add(self, s_sy_user_id, dt_create_date_time, data, options,
#         analyse_type):
#     self.s_sy_user_id = s_sy_user_id
#     self.dt_create_date_time = dt_create_date_time
#     self.js_data = data
#     self.s_options = options
#     self.s_analyse_type = analyse_type
#
#     db.session.add(self)
#     db.session.commit()
#
# def to_dict(self):
#     return {
#         'id': self.id,
#         'data': self.data,
#         'options': self.options,
#         'analyse_type': self.analyse_type,
#         'time': self.dt_create_date_time
#     }
#
# def to_json_history_query(self):
#     return {
#         'id': self.id,
#         'options': self.options,
#         'analyse_type': self.analyse_type,
#         'time': self.dt_create_date_time
#     }
