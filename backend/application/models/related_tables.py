"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: related_tables.py
@time: 2021/1/29 21:37
@desc:
"""
from application.extensions import db

target_gene_table = db.Table(
    "tb_rel_target_gene",
    db.metadata,
    db.Column(
        "target_id",
        db.String(36),
        db.ForeignKey("tb_target.bin_id", ondelete="CASCADE"),
    ),
    db.Column(
        "ingredient_id",
        db.String(36),
        db.ForeignKey("tb_ingredient.bin_id", ondelete="CASCADE"),
    ),
    db.Column("s_name", db.String(100), comment="关系名", default="TargetGene"),
)

herb_tcm_table = db.Table(
    "tb_rel_herb_tcm",
    db.metadata,
    db.Column(
        "herb_id", db.String(36), db.ForeignKey("tb_herb.bin_hid", ondelete="CASCADE")
    ),
    db.Column(
        "tcm_id",
        db.String(36),
        db.ForeignKey("tb_tcm_symptom.bin_id", ondelete="CASCADE"),
    ),
    db.Column("s_name", db.String(100), comment="关系名", default="HerbTCM"),
)

herb_gene_table = db.Table(
    "tb_rel_herb_gene",
    db.metadata,
    db.Column(
        "herb_id", db.String(36), db.ForeignKey("tb_herb.bin_hid", ondelete="CASCADE")
    ),
    db.Column(
        "ingredient_id",
        db.String(36),
        db.ForeignKey("tb_ingredient.bin_id", ondelete="CASCADE"),
    ),
    db.Column("s_name", db.String(100), comment="关系名", default="HerbIngredient"),
)

target_disease_table = db.Table(
    "tb_rel_target_disease",
    db.metadata,
    db.Column(
        "target_id",
        db.String(36),
        db.ForeignKey("tb_target.bin_id", ondelete="CASCADE"),
    ),
    db.Column(
        "disease_id",
        db.String(36),
        db.ForeignKey("tb_disease.bin_id", ondelete="CASCADE"),
    ),
    db.Column("s_name", db.String(100), comment="关系名", default="GeneIndications"),
)

tcm_mm_table = db.Table(
    "tb_rel_tcm_mm",
    db.metadata,
    db.Column(
        "tcm_id",
        db.String(36),
        db.ForeignKey("tb_tcm_symptom.bin_id", ondelete="CASCADE"),
    ),
    db.Column(
        "mm_id",
        db.String(36),
        db.ForeignKey("tb_mm_symptom.bin_id", ondelete="CASCADE"),
    ),
    db.Column("s_name", db.String(100), comment="关系名", default="TCM2MM"),
)

mm_disease_table = db.Table(
    "tb_rel_mm_disease",
    db.metadata,
    db.Column(
        "mm_id",
        db.String(36),
        db.ForeignKey("tb_mm_symptom.bin_id", ondelete="CASCADE"),
    ),
    db.Column(
        "disease_id",
        db.String(36),
        db.ForeignKey("tb_disease.bin_id", ondelete="CASCADE"),
    ),
    db.Column("s_name", db.String(100), comment="关系名", default="MM2Dis"),
)
