"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: symptom.py
@time: 2021/1/24 18:25
@desc:
"""
from sqlalchemy import Integer, Column, String

from application.extensions import db
from application.models.base import BaseModel
from application.models.disease import Disease
from application.models.related_tables import (
    herb_tcm_table,
    tcm_mm_table,
    mm_disease_table,
)
from application.utils.normal import gen_id


class MMSymptom(BaseModel):
    """
    Manual curation to the UMLS database

    The SMMS file in tabular format includes all descriptive information
     about 961 MM symptoms recorded in SymMap. The details of each column are
      as follows:

    MM_symptom_id：the primary ID of each MM symptom recorded in SymMap.
    MM_symptom_name: the name of each MM symptom.
    MM_symptom_definition: the definition of each MM symptom.
    MeSH_tree_numbers: the hierarchical classification of each MM symptom in
     tree numbers from the MeSH database.
    Alias: multiple aliases separated by a ‘|’ for each MM symptom collected
     from diverse resources.
    UMLS_id: the cross reference of each MM symptom in the UMLS database.
    OMIM_id: the cross reference of each MM symptom in the OMIM database.
    ICD10CM_id: the cross reference of each MM symptom in the ICD (tenth
     clinical modification) database.
    HPO_id: the cross reference of each MM symptom in the HPO database.
    MeSH_id: the cross reference of each MM symptom in the MeSH database.
    The SMMS key file in tabular format includes all the search terms about
     961 MM symptoms recorded in SymMap. The details of each column are as
      follows:

    MM_symptom_id：the primary ID of each MM symptom recorded in SymMap.
    Field_name: the search field of the MM symptom table, including the
     MM_symptom_name, UMLS_id and the alias.
    Field_context：the search terms of all MM symptoms recorded in SymMap.
    """

    __tablename__ = "tb_mm_symptom"
    bin_id = Column(String(32), primary_key=True)
    s_name = Column(String(50), default="")
    s_mm_symptom_definition = Column(String(1000), default="")
    s_mm_tree_numbers = Column(String(1000), default="")

    fk_disease = db.relationship(
        "Disease",
        secondary=mm_disease_table,
        backref=db.backref("fk_mm", lazy="dynamic"),
    )

    def __init__(self):
        self.bin_id = gen_id()

    def add(self, data):
        data["i_status"] = 1

        fk_disease = []
        for rel in data["rels"].split(","):
            tmp = Disease.query.filter_by(s_mark=rel).first()
            if tmp:
                fk_disease.append(tmp)
        if fk_disease:
            self.fk_disease = fk_disease

        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.bin_id,
            "s_name": self.s_name,
            "s_mm_symptom_definition": self.s_mm_symptom_definition,
            "s_mm_tree_numbers": self.s_mm_tree_numbers,
            "disease": ",".join([foo.s_name for foo in self.fk_disease]),
        }

    def to_dict_particular(self):
        return {
            "id": self.bin_id,
            "s_name": self.s_name,
            "s_mm_symptom_definition": self.s_mm_symptom_definition,
            "s_mm_tree_numbers": self.s_mm_tree_numbers,
            "disease": ",".join([foo.s_name for foo in self.fk_disease]),
        }


class TCMSymptom(BaseModel):
    """
    Chinese pharmacopoeia (2015)

    The SMTS file in tabular format includes all descriptive information about
     1,717 TCM symptoms recorded in SymMap. The details of each column are as
      follows:

    TCM_symptom_id: the primary ID of each TCM symptom recorded in SymMap.
    TCM_symptom_name: the name of TCM symptoms in Chinese.
    Symptom_pinyin_name: the name of TCM symptoms in Pinyin.
    Symptom_definition: the definition of TCM symptoms using the terms from
     traditional Chinese medicine.
    Symptom_locus: the locus of TCM symptoms using the terms from traditional
     Chinese medicine.
    Symptom_property: the property of TCM symptoms using the terms from
     traditional Chinese medicine.
    The SMTS key file in tabular format includes all the search terms about
     1,717 TCM symptoms recorded in SymMap. The details of each column are
      as follows:

    TCM_symptom_id: the primary ID of each TCM symptom recorded in SymMap.
    Field_name: the search field of the TCM symptom table, including the
     TCM_symptom_name and the symptom_pinyin_name.
    Field_context：the search terms of all TCM symptoms recorded in SymMap.
    """

    __tablename__ = "tb_tcm_symptom"
    bin_id = Column(String(32), primary_key=True)
    s_name = Column(String(50), default="")
    s_pinyin_name = Column(String(50), default="")
    s_symptom_definition = Column(String(1000), default="")
    s_symptom_locus = Column(String(50), comment="病位", default="")
    s_symptom_property = Column(String(100), default="")

    fk_mm = db.relationship(
        "MMSymptom",
        secondary=tcm_mm_table,
        backref=db.backref("fk_tcm", lazy="dynamic"),
    )

    def __init__(self):
        self.bin_id = gen_id()

    def add(self, data):
        data["i_status"] = 1

        fk_mm = []
        for rel in data["rels"].split(","):
            tmp = MMSymptom.query.filter_by(s_mark=rel).first()
            if tmp:
                fk_mm.append(tmp)
        if fk_mm:
            self.fk_mm = fk_mm

        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.bin_id,
            "s_name": self.s_name,
            "s_pinyin_name": self.s_pinyin_name,
            "s_symptom_definition": self.s_symptom_definition,
            "s_symptom_locus": self.s_symptom_locus,
            "s_symptom_property": self.s_symptom_property,
            "mm": ",".join([foo.s_name for foo in self.fk_mm]),
        }

    def to_dict_particular(self):
        return {
            "id": self.bin_id,
            "s_name": self.s_name,
            "s_pinyin_name": self.s_pinyin_name,
            "s_symptom_definition": self.s_symptom_definition,
            "s_symptom_locus": self.s_symptom_locus,
            "s_symptom_property": self.s_symptom_property,
            "mm": ",".join([foo.s_name for foo in self.fk_mm]),
        }
