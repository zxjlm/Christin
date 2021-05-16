"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: target.py
@time: 2021/1/24 18:12
@desc:
"""
from sqlalchemy import Column, String

from application.extensions import db
from application.models.base import BaseModel
from application.models.disease import Disease
from application.models.related_tables import target_disease_table
from application.utils.normal import gen_id


class Target(BaseModel):
    """
    Integration of HIT, TCMSP, HPO, DrugBank and NCBI database

    The SMTT file in tabular format includes all descriptive information about 4,302 targets recorded in SymMap. The details of each column are as follows:

    Target_id：the primary ID of each target recorded in SymMap.
    Gene_symbol: the gene symbol of each target.
    Chromosome: the chromosome number in which each target located.
    Gene_name: the gene name of each target.
    Protein_name: the protein name of each target.
    Alias: multiple aliases separated by a ‘|’ for each target collected
     from diverse resources.
    HIT_id: the cross reference of each target in the HIT database.
    TCMSP_id: the cross reference of each target in the TCMSP database.
    Ensembl_id: the cross reference of each target in the Ensembl database.
    NCBI_id: the cross reference of each target in the NCBI database.
    HGNC_id: the cross reference of each target in the HGNC database.
    Vega_id: the cross reference of each target in the Vega database.
    GenBank_Gene_id: the cross reference of each target in the GenBank_Gene
     database.
    GenBank_Protein_id: the cross reference of each target in the
     GenBank_Protein database.
    Uniprot_id: the cross reference of each target in the Uniprot database.
    PDB_id: the cross reference of each target in the PDB database.
    OMIM_id: the cross reference of each target in the OMIM database.
    miRBase_id: the cross reference of each target in the miRBase database.
    IMGT/GENE-DB_id: the cross reference of each target in the IMGT/GENE-DB
     database.
    The SMTT key file in tabular format includes all the search terms about
     4,302 targets recorded in SymMap. The details of each column are
      as follows:

    Target_id ：the primary ID of each target recorded in SymMap.
    Field_name: the search field of the target table, including the
     gene_symbol, gene_name, protein_name, alias and the Ensembl_id.
    Field_context：the search terms of all target recorded in SymMap.
    """

    __tablename__ = "tb_target"
    bin_id = Column(String(32), primary_key=True)
    s_gene_symbol = Column(String(50), default="")
    s_chromosome = Column(String(20), default="")
    s_name = Column(String(500), default="")
    s_protein_name = Column(String(500), default="")

    fk_disease = db.relationship(
        "Disease",
        secondary=target_disease_table,
        backref=db.backref("fk_target", lazy="dynamic"),
    )

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

    def __init__(self):
        self.bin_id = gen_id()

    def to_dict(self):
        return {
            "id": self.bin_id,
            "s_gene_symbol": self.s_gene_symbol,
            "s_chromosome": self.s_chromosome,
            "s_name": self.s_name,
            "s_protein_name": self.s_protein_name,
            "disease": ",".join([foo.s_name for foo in self.fk_disease]),
        }

    def to_dict_particular(self):
        return {
            "id": self.bin_id,
            "s_gene_symbol": self.s_gene_symbol,
            "s_chromosome": self.s_chromosome,
            "s_name": self.s_name,
            "s_protein_name": self.s_protein_name,
            "disease": ",".join([foo.s_name for foo in self.fk_disease]),
        }
