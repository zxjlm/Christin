"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: ingredient.py
@time: 2021/1/24 18:22
@desc:
"""
from sqlalchemy import Column, String, Float, Text

from application.extensions import db
from application.models.base import BaseModel
from application.models.related_tables import target_gene_table, herb_gene_table
from application.models.target import Target
from application.utils.normal import gen_id


class Ingredient(BaseModel):
    """
    Integration of TCMID, TCMSP and TCM-ID database

    The SMIT file in tabular format includes all descriptive information about
     19,595 ingredients recorded in SymMap. The details of each column are
      as follows:

    Ingredient_id：the primary ID of each ingredient recorded in SymMap.
    Molecule_name：the common name of each ingredient. Generally, we selected
     the first name appeared in the PubChem database.
    Molecule_formula: the molecule formula for each ingredient.
    Molecule_weight: the molecule weight for each ingredient.
    OB_score：the oral bioavailability score for each ingredient.
    Alias: multiple aliases separated by a ‘|’ for each ingredient collected
     from diverse resources.
    PubChem_id: the cross reference of each ingredient in the PubChem database.
    CAS_id: the cross reference of each ingredient in the CAS database.
    TCMID_id: the cross reference of each ingredient in the TCMID database.
    TCM-ID_id: the cross reference of each ingredient in the TCM-ID database.
    TCMSP_id: the cross reference of each ingredient in the TCMSP database.
    The SMIT key file in tabular format includes all the search terms about
     19,595 ingredients recorded in SymMap. The details of each column are
      as follows:

    Ingredient_id：the primary ID of each ingredient recorded in SymMap.
    Field_name: the search field of the ingredient table, including the
     molecule_name, alias and the CAS_id.
    Field_context：the search terms of all ingredient recorded in SymMap.
    """

    __tablename__ = "tb_ingredient"
    bin_id = Column(String(32), primary_key=True, comment='id')
    s_name = Column(String(500), default="", comment='成分名称')
    s_molecule_formula = Column(String(255), default="", comment='分子式')
    f_molecule_weight = Column(Float, default=-1.0, comment='分子权重')
    f_ob_score = Column(Float, default=-1.0, comment='每种成分的口服生物利用度得分')
    s_alias = Column(Text, default="", comment='别名')

    fk_target = db.relationship(
        "Target",
        secondary=target_gene_table,
        backref=db.backref("fk_target_ingredient", lazy="dynamic"),
    )

    def __init__(self):
        self.bin_id = gen_id()

    def add(self, data):
        data["i_status"] = 1
        data["f_ob_score"] = float(data["f_ob_score"]) if data["f_ob_score"] else -1.0
        data["f_molecule_weight"] = (
            float(data["f_molecule_weight"]) if data["f_molecule_weight"] else -1.0
        )

        fk_target = []
        for rel in data["rels"].split(","):
            tmp = Target.query.filter_by(s_mark=rel).first()
            if tmp:
                fk_target.append(tmp)
        if fk_target:
            self.fk_target = fk_target

        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.bin_id,
            "s_name": self.s_name,
            "s_molecule_formula": self.s_molecule_formula,
            "f_molecule_weight": self.f_molecule_weight,
            "f_ob_score": self.f_ob_score,
            "s_alias": self.s_alias,
            "target": ",".join([foo.s_name for foo in self.fk_target]),
        }

    def to_dict_particular(self):
        return {
            "id": self.bin_id,
            "s_name": self.s_name,
            "s_molecule_formula": self.s_molecule_formula,
            "f_molecule_weight": self.f_molecule_weight,
            "f_ob_score": self.f_ob_score,
            "s_alias": self.s_alias,
            "target": ",".join([foo.s_name for foo in self.fk_target]),
        }
