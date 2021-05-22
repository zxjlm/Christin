# -*- coding:utf-8 -*-
from sqlalchemy import ForeignKey, Column, Integer, String, Float
from sqlalchemy.orm import relationship

__author__ = "harumonia"

from application.extensions import db
from application.models.base import BaseModel


class PrescriptionAlias(BaseModel):
    """
    别名
    """

    __tablename__ = "tb_prescription_alias"
    id = Column(Integer, autoincrement=True, primary_key=True)
    bin_pid = Column(
        String(32), ForeignKey("tb_prescription.bin_pid", ondelete="CASCADE")
    )
    s_alias = Column(String(20), comment=u"别名", nullable=False)


class PrescriptionIndications(BaseModel):
    """
    主治
    """

    __tablename__ = "tb_prescription_indications"
    id = Column(Integer, autoincrement=True, primary_key=True)
    # tb_prescription = relationship('Prescription')
    bin_pid = Column(
        String(32), ForeignKey("tb_prescription.bin_pid", ondelete="CASCADE")
    )
    s_indications = Column(String(500), comment=u"主治")


class PrescriptionConstitute(BaseModel):
    """
    组成
    """

    __tablename__ = "tb_prescription_constitute"
    id = Column(Integer, autoincrement=True, primary_key=True)
    # tb_prescription = relationship('Prescription')
    bin_pid = Column(
        String(32), ForeignKey("tb_prescription.bin_pid", ondelete="CASCADE")
    )
    bin_hid = Column(String(32))
    s_herb_name = Column(String(10), nullable=False)
    f_dose = Column(Float, comment=u"剂量")  # 是否为区间
    s_method = Column(String(10), comment=u"煎法")  # 煎法
    s_unit = Column(String(10), comment=u"单位")

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.add(self)
        db.session.commit()
