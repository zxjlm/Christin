# -*- coding:utf-8 -*-

__author__ = "harumonia"

from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from application.extensions import db
from application.models.base import BaseModel

# class Meridian(BaseModel):
#     """
#     归经
#     """
#     __tablename__ = 'tb_herb_meridian'
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     tb_herb = relationship('Herb')
#     bin_hid = Column(String(32),
#                      ForeignKey('tb_herb.bin_hid', ondelete='CASCADE'))
#     type_id = Column(Integer)
#     s_meridian = Column(String(20), comment=u"归经", nullable=False)  # 归经

herb_property_table = db.Table(
    "tb_rel_herb_property",
    db.metadata,
    db.Column(
        "herb_id", db.String(36), db.ForeignKey("tb_herb.bin_hid", ondelete="CASCADE")
    ),
    db.Column(
        "property_id", BigInteger, db.ForeignKey("tb_dic_data.id", ondelete="CASCADE")
    ),
)


# class FourNatures(BaseModl):
#     """
#     四气
#     """
#     __tablename__ = 'tb_herb_four_natures'
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     tb_herb = relationship('Herb')
#     bin_hid = Column(String(32),
#                      ForeignKey('tb_herb.bin_hid', ondelete='CASCADE'))
#     type_id = Column(Integer)
#     s_four_natures = Column(String(10), comment=u"四气", nullable=False)


# class HerbAffiliate(BaseModel):
#     """
#     附药
#     """
#     __tablename__ = 'tb_herb_affiliate'
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     tb_herb = relationship('Herb')
#     bin_hid = Column(String(32),
#                      ForeignKey('tb_herb.bin_hid', ondelete='CASCADE'))
#     s_HerbAffiliate = Column(String(20), nullable=False, comment="附药的名字")


# class FiveTastes(BaseModel):
#     """
#     五味
#     """
#     __tablename__ = 'tb_herb_five_tastes'
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     tb_herb = relationship('Herb')
#     bin_hid = Column(String(32),
#                      ForeignKey('tb_herb.bin_hid', ondelete='CASCADE'))
#     type_id = Column(Integer)
#     s_five_tastes = Column(String(10), comment=u"五味", nullable=False)
#
#
# class FloatingAndSinking(BaseModel):
#     """
#     升降浮沉
#     """
#     __tablename__ = 'tb_herb_floating_and_sinking'
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     tb_herb = relationship('Herb')
#     bin_hid = Column(String(32),
#                      ForeignKey('tb_herb.bin_hid', ondelete='CASCADE'))
#     type_id = Column(Integer)
#     s_floating_and_sinking = Column(String(10), comment=u"升降浮沉")


class HerbAlias(BaseModel):
    """
    别名
    """

    __tablename__ = "tb_herb_alias"
    id = Column(Integer, autoincrement=True, primary_key=True)
    # tb_herb = relationship('Herb')
    bin_hid = Column(String(32), ForeignKey("tb_herb.bin_hid", ondelete="CASCADE"))
    s_herb_alias = Column(String(20), comment=u"别名", nullable=False)


class HerbIndications(BaseModel):
    """
    主治
    """

    __tablename__ = "tb_herb_indications"
    id = Column(Integer, autoincrement=True, primary_key=True)
    tb_herb = relationship("Herb")
    bin_hid = Column(String(32), ForeignKey("tb_herb.bin_hid", ondelete="CASCADE"))
    s_herb_indications = Column(String(20), comment=u"主治", nullable=False)


class HerbEffect(BaseModel):
    """
    功效
    """

    __tablename__ = "tb_herb_effect"
    id = Column(Integer, autoincrement=True, primary_key=True)
    tb_herb = relationship("Herb")
    bin_hid = Column(String(32), ForeignKey("tb_herb.bin_hid", ondelete="CASCADE"))
    s_herb_effect = Column(String(20), comment=u"功效", nullable=False)
