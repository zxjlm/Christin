# -*- coding:utf-8 -*-

__author__ = "harumonia"

from sqlalchemy import String, Integer, Column, Text, JSON, DateTime
from sqlalchemy.orm import relationship, backref

from application.models.base import BaseModel
from application.utils.normal import gen_id


class Prescription(BaseModel):
    __tablename__ = "tb_prescription"
    bin_pid = Column(String(32), primary_key=True, default=gen_id())
    # i_board_head = Column(Integer, default=0)
    # s_board_head = Column(String(20), nullable=True)
    # i_subclass = Column(Integer, default=0)
    # s_subclass = Column(String(20), default="")
    s_name = Column(String(20), comment=u"名字", nullable=False)
    s_abbreviated_name = Column(String(100), comment=u"首字母缩写", default="")
    constitute = relationship(
        "PrescriptionConstitute",
        backref=backref("prescription"),
        cascade="save-update,delete",
    )
    s_alias = relationship(
        "PrescriptionAlias",
        backref=backref("prescription"),
        cascade="save-update,delete",
    )
    indications = relationship(
        "PrescriptionIndications",
        backref=backref("prescription"),
        cascade="save-update,delete",
    )
    # dose_list = Column(String(50), comment=u"用量列表")
    s_dosage_form = Column(String(10), comment=u"剂型", default="")
    s_indications = Column(String(500), comment=u"主治", default="")
    s_origin = Column(String(255), comment=u"出处", default="")
    s_usage = Column(Text, comment=u"用法", default="")
    s_modified = Column(String(500), comment=u"加减", default="")
    s_complain = Column(String(1500), comment=u"方解", default="")
    s_function = Column(String(255), comment=u"功用", default="")
    s_compatibility = Column(String(500), comment=u"宜忌", default="")
    s_discussion = Column(Text, comment=u"各家论述", default="")
    s_warning = Column(Text, comment=u"用药禁忌", default="")
    s_bad_effect = Column(String(500), comment=u"不良反应", default="")
    s_clinic = Column(Text, comment=u"临床应用", default="")
    s_pharmacological_action = Column(Text, comment=u"药理作用", default="")
    s_prison = Column(String(500), comment=u"毒性实验", default="")
    s_chemical_component = Column(String(500), comment=u"化学成分", default="")
    s_physicochemical_property = Column(String(500), comment=u"理化性质", default="")
    s_manufacturer = Column(Text, comment=u"生产厂家", default="")
    s_normal_remark = Column(Text, comment=u"普通备注", default="")
    json_remark = Column(JSON, comment=u"Json备注", default="")

    def __init__(self):
        self.bin_hid = gen_id()

    def to_dict(self):
        return {
            "id": self.bin_pid,
            "s_name": self.s_name,
            "s_en_name": "",
            # 'constitute': ','.join(
            #     [foo.s_herb_name for foo in self.constitute]),
            # 'alias': ','.join([foo.s_alias for foo in self.s_alias]),
        }

    def to_dict_particular(self):
        return {
            "s_name": self.s_name,
            "s_abbreviated_name": self.s_abbreviated_name,
            "s_dosage_form": self.s_dosage_form,
            "s_indications": self.s_indications,
            "s_origin": self.s_origin,
            "s_modified": self.s_modified,
            "s_complain": self.s_complain,
            "s_function": self.s_function,
            "s_compatibility": self.s_compatibility,
            "s_bad_effect": self.s_bad_effect,
            "s_prison": self.s_prison,
            "s_chemical_component": self.s_chemical_component,
            "s_physicochemical_property": self.s_physicochemical_property,
            "s_clinic": self.s_clinic,
            "s_pharmacological_action": self.s_pharmacological_action,
            "s_usage": self.s_usage,
            "s_discussion": self.s_discussion,
            "s_warning": self.s_warning,
            "s_manufacturer": self.s_manufacturer,
            "s_normal_remark": self.s_normal_remark,
            "json_remark": self.json_remark,
            "constitute": ",".join([foo.s_herb_name for foo in self.constitute]),
            "alias": ",".join([foo.s_alias for foo in self.s_alias]),
        }

    #
    # def to_json_show_for_visitor(self):
    #     return {
    #         'id': self.bin_pid,
    #         'name': self.s_name,
    #         'constitute': ','.join(
    #             [foo.s_herb_name for foo in self.constitute]),
    #         'alias': ','.join([foo.s_alias for foo in self.s_alias]),
    #         'board_head': self.s_board_head,
    #         'subclass': self.s_subclass
    #     }
