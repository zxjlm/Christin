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
