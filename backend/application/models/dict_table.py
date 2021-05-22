# -*- coding:utf-8 -*-
from sqlalchemy import ForeignKey, Integer, Column, String, BigInteger
from sqlalchemy.orm import relationship

__author__ = "harumonia"

from application.extensions import db
from application.models.base import BaseModel


class DicTableType(BaseModel):
    __tablename__ = "tb_dic_type"
    id = Column(Integer, autoincrement=True, primary_key=True)
    s_name = Column(String(20), nullable=True)
    s_en_name = Column(String(100))

    def __init__(self):
        # 初始化字典表说明
        pass

    @staticmethod
    def content():
        """
        1.药材大类  herb_broadHeading
        2.药材小类  herb_subclass
        3.方剂大类  prescription_broadHeading
        4.方剂小类  prescription_subclass
        5.四气    four_natures
        6.五味    five_tastes
        7.升降浮沉  floating_and_sinking
        8.归经    meridian
        9.节点标签 node
        10.节点关系 relation
        Returns:

        """
        dict1 = [
            {1: "herb_broad_heading"},
            {2: "herb_subclass"},
            {3: "prescription_broad_heading"},
            {4: "prescription_subclass"},
            {5: "four_natures"},
            {6: "five_tastes"},
            {7: "floating_and_sinking"},
            {8: "meridians"},
            {9: "node"},
            {10: "relation"},
        ]
        return dict1


class DicTableData(BaseModel):
    __tablename__ = "tb_dic_data"
    id = Column(BigInteger, autoincrement=True, nullable=False, primary_key=True)
    fk_dic_type = relationship("DicTableType")
    type_id = Column(Integer, ForeignKey("tb_dic_type.id"), comment="对应字典表的类型id")
    s_name = Column(String(20), comment="具体的数值", nullable=False, unique=True)
    s_en_name = Column(String(50), comment="英文名")
    # s_head_sub_cascade = Column(String(20), default="", nullable=False,
    #                             comment="内部级联关系")
    s_remark = Column(String(20), default="", comment="备注")

    def add(self, data):
        dic_type = DicTableType.query.get(int(data["type_name"]))
        self.fk_dic_type = dic_type
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

    def to_dict(self):
        return {
            "id": self.id,
            "s_name": self.s_name,
            "s_en_name": self.s_en_name,
            "type_name": self.fk_dic_type.s_name,
            "s_remark": self.s_remark,
        }

    def to_dict_particular(self):
        return {
            "id": self.id,
            "s_name": self.s_name,
            "s_en_name": self.s_en_name,
            "type_name": str(self.fk_dic_type.id),
            "s_remark": self.s_remark,
        }
