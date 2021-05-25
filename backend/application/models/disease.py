"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: disease.py
@time: 2021/1/24 18:17
@desc:
"""
from sqlalchemy import Column, String

from application.models.base import BaseModel
from application.utils.normal import gen_id


class Disease(BaseModel):
    """
    Integration of OMIM, MeSH and Orphanet database

    The SMDE file in tabular format includes all descriptive information
     about 5,235 diseases recorded in SymMap. The details of each column
      are as follows:

    Disease_id: the primary ID of each disease recorded in SymMap.
    Disease_name: the name of each disease.
    Disease_definition: the definition for some diseases.
    Alias: multiple aliases separated by a ‘|’ for each disease collected
    from diverse resources.
    MeSH_id: the cross reference of each disease in the MeSH database.
    OMIM_id: the cross reference of each disease in the OMIM database.
    Orphanet_id: the cross reference of each disease in the Orphanet database.
    ICD10CM_id: the cross reference of each disease in the ICD (tenth clinical
     modification) database.
    UMLS_id: the cross reference of each disease in the UMLS database.
    MedDRA_id: the cross reference of each disease in the MedDRA database.
    The SMDE key file in tabular format includes all the search terms about
     5,235 diseases recorded in SymMap. The details of each column are
      as follows:

    Disease_id: the primary ID of each disease recorded in SymMap.
    Field_name: the search field of the disease table, including the
     disease_name and the alias.
    Field_context：the search terms of all disease recorded in SymMap.
    """

    __tablename__ = "tb_disease"
    bin_id = Column(String(32), primary_key=True, comment='id')
    s_name = Column(String(500), default="", comment='疾病名称')
    s_disease_definition = Column(String(1000), default="", comment='疾病定义')

    def __init__(self):
        self.bin_id = gen_id()

    def to_dict(self):
        return {
            "id": self.bin_id,
            "s_name": self.s_name,
            "s_disease_definition": self.s_disease_definition,
        }

    def to_dict_particular(self):
        return {
            "id": self.bin_id,
            "s_name": self.s_name,
            "s_disease_definition": self.s_disease_definition,
        }
