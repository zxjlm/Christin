# -*- coding:utf-8 -*-
from sqlalchemy import Text, String, JSON

__author__ = "harumonia"

from application.extensions import db
from application.models.base import BaseModel
from application.models.dict_table import DicTableData
from application.models.herb.sub_herb import herb_property_table, HerbAlias
from application.models.ingredient import Ingredient
from application.utils.custom_exceptions import UnknownValueException
from application.models.related_tables import herb_tcm_table, herb_gene_table
from application.models.symptom import TCMSymptom
from application.utils.neo4j_handler import (
    neo_data_update_trigger,
    neo_data_create_trigger,
)
from application.utils.normal import gen_id


class Herb(BaseModel):
    __tablename__ = "tb_herb"
    bin_hid = db.Column(String(32), primary_key=True)
    # i_board_head = db.Column(Integer, default=0)
    # i_subclass = db.Column(Integer, default=0)
    s_name = db.Column(String(10), unique=True, nullable=False)
    s_en_name = db.Column(String(100), comment="英文名", default="")

    fk_alias = db.relationship(
        "HerbAlias", backref=db.backref("fk_herb"), cascade="save-update,delete"
    )
    fk_indications = db.relationship(
        "HerbIndications", backref=db.backref("fk_herb"), cascade="save-update,delete"
    )
    fk_effect = db.relationship(
        "HerbEffect", backref=db.backref("fk_herb"), cascade="save-update,delete"
    )

    fk_property = db.relationship(
        "DicTableData", secondary=herb_property_table, backref=db.backref("fk_herb")
    )

    # meridian = db.relationship('Meridian',
    #                            backref=db.backref('herb'),
    #                            cascade='save-update,delete')
    # four_properties = db.relationship('FourNatures',
    #                                   backref=db.backref('herb'),
    #                                   cascade='save-update,delete')
    # five_tastes = db.relationship('FiveTastes', backref=db.backref('herb'),
    #                               cascade='save-update,delete')
    # ascending_descending_sinking_floating = db.relationship(
    #     'FloatingAndSinking', backref=db.backref('herb'),
    #     cascade='save-update,delete')

    s_latin_name = db.Column(String(100), comment="拉丁文名", default="")
    s_abbreviated_name = db.Column(String(20), comment=u"首字母缩写", default="")
    s_usage = db.Column(String(500), comment=u"用法用量", default="")
    s_herb_affiliate = db.Column(String(20), comment="附药的名字", default="")
    s_origin = db.Column(String(200), comment=u"出处", default="")
    s_application = db.Column(String(500), comment=u"应用", default="")
    s_foundation = db.Column(Text, comment=u"基原", default="")
    s_prison = db.Column(Text, comment=u"毒性", default="")
    s_ancient_literature = db.Column(String(500), comment=u"古代文献", default="")
    s_chemical = db.Column(Text, comment=u"化学成分", default="")
    s_discussion = db.Column(db.Text, comment=u"各家论述", default="")
    s_affiliate = db.Column(Text, comment=u"附方", default="")
    s_pharmacological_action = db.Column(Text, comment=u"药理作用", default="")
    s_untoward_effect = db.Column(Text, comment="不良反应", default="")
    s_normal_remark = db.Column(String(500), comment=u"普通备注", default="")
    json_remark = db.Column(JSON, comment="Json备注", default="")

    fk_tcm = db.relationship(
        "TCMSymptom", secondary=herb_tcm_table, backref=db.backref("fk_herb")
    )

    fk_ingredient = db.relationship(
        "Ingredient", secondary=herb_gene_table, backref=db.backref("fk_herb")
    )

    def __init__(self):
        self.bin_hid = gen_id()

    @staticmethod
    def cls_fk():
        """
        类的外键
        Returns:

        """
        return {
            "four_natures": [],
            "five_tastes": [],
            "floating_and_sinking": [],
            "meridians": [],
            "herb_broad_heading": "",
            "herb_subclass": "",
        }

    def to_dict(self):
        # xing_list = FourNatures.query.filter_by(bin_hid=self.bin_hid).all()

        res = {
            "id": self.bin_hid,
            "s_name": self.s_name,
            "s_en_name": self.s_en_name,
        }

        return res

    def fk_processor_output(self):
        properties = self.fk_property
        property_dict = self.cls_fk()
        for sub_property in properties:
            if isinstance(property_dict[sub_property.fk_dic_type.s_en_name], list):
                property_dict[sub_property.fk_dic_type.s_en_name].append(
                    str(sub_property.id)
                )
            elif isinstance(property_dict[sub_property.fk_dic_type.s_en_name], str):
                property_dict[sub_property.fk_dic_type.s_en_name] = str(sub_property.id)
        return property_dict

    def fk_processor_input(self, fk_data: dict):
        """
        录入数据时，对外键数据进行拆解

        TODO: 添加数据验证(针对错位数据)
        Args:
            fk_data:

        Returns:

        """
        self.fk_property = []
        property_dict = self.cls_fk()
        for k, v in fk_data.items():
            if isinstance(property_dict[k], list):
                if not v:
                    continue
                values = v.split(",")
                for value in values:
                    query_res = DicTableData.query.get(int(value))
                    if query_res:
                        self.fk_property.append(query_res)
                        property_dict[k].append(query_res.s_name)
                    else:
                        raise UnknownValueException("unknown data")
            elif isinstance(property_dict[k], str):
                if not v:
                    continue
                query_res = DicTableData.query.get(int(v))
                if query_res:
                    self.fk_property.append(query_res)
                    property_dict[k] = query_res.s_name
                else:
                    raise UnknownValueException("unknown data")

        for k, v in property_dict.items():
            if isinstance(v, list):
                property_dict[k] = ",".join(v)

        return property_dict

    def to_dict_particular(self):
        property_dict = self.fk_processor_output()
        # for k, v in property_dict.items():
        #     property_dict[k] = ','.join(v)
        res = {
            "id": self.bin_hid,
            "s_name": self.s_name,
            "s_en_name": self.s_en_name,
            "s_latin_name": self.s_latin_name,
            "s_abbreviated_name": self.s_abbreviated_name,
            "s_usage": self.s_usage,
            "s_herb_affiliate": self.s_herb_affiliate,
            "s_origin": self.s_origin,
            "s_application": self.s_application,
            "s_foundation": self.s_foundation,
            "s_prison": self.s_prison,
            "s_ancient_literature": self.s_ancient_literature,
            "s_chemical": self.s_chemical,
            "s_discussion": self.s_discussion,
            "s_affiliate": self.s_affiliate,
            "s_pharmacological_action": self.s_pharmacological_action,
            "s_untoward_effect": self.s_untoward_effect,
            "s_normal_remark": self.s_normal_remark,
            "json_remark": self.json_remark,
            **property_dict,
        }

        return res

    def add(self, data):
        def get_property(cls, pro_list):
            fk_tcmm = []
            for rell in pro_list:
                tmpp = cls.query.filter_by(s_name=rell).first()
                if tmpp:
                    fk_tcmm.append(tmpp)
            return fk_tcmm

        def get_property_1(cls, pro_list):
            """
            针对symmap数据集开发的属性提取方法
            Args:
                cls:
                pro_list:

            Returns:

            """
            fk_tcmm = []
            for rell in pro_list:
                tmpp = cls.query.filter_by(s_mark=rell).first()
                if tmpp:
                    fk_tcmm.append(tmpp)
            return fk_tcmm

        def get_alia(alia_list):
            herb_alia_list = []
            for alia in alia_list:
                herb_alia_list.append(HerbAlias().add({"s_herb_alias": alia}))
            return herb_alia_list

        data["i_status"] = 1
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        if "s_properties" in data:
            properties = data["s_properties"].split(",")
            self.fk_property = get_property(DicTableData, properties)

        if "rels" in data:
            self.fk_tcm = get_property_1(TCMSymptom, data["rels"].split(","))

            self.fk_ingredient = get_property_1(Ingredient, data["rels"].split(","))

        if "alias" in data:
            self.fk_alias = get_alia(data["alias"].split(","))

        db.session.add(self)
        neo_data_create_trigger("Herb", data)
        db.session.commit()

    def update(self, data: dict):
        fk_dic = self.cls_fk()
        for key, value in data.items():
            if key in fk_dic:
                fk_dic[key] = data[key]
            if hasattr(self, key) and key != "bin_hid":
                setattr(self, key, value)
        property_dict = self.fk_processor_input(fk_dic)
        data.update(**property_dict)
        db.session.add(self)
        neo_data_update_trigger("Herb", data)
        db.session.commit()

    def extract_json(self, json_req: dict):
        """
        从json文件中提取数据
        Args:
            json_req:

        Returns:

        """
        extract_data = {
            "type": "HERB",
            "s_name": json_req.get("name", ""),
            "s_latin_name": json_req.get("latin_name", ""),
            "s_en_name": json_req.get("en_name", ""),
            "s_origin": json_req.get("origin", ""),
            "s_application": json_req.get("application", ""),
        }
        return {k: v for k, v in extract_data.items() if v}
