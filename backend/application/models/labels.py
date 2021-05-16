"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: labels.py
@time: 2021/5/5 9:19 上午
@desc:
"""
from sqlalchemy import Integer, Column, String

from application.models.base import BaseModel


class Labels(BaseModel):
    __tablename__ = "tb_labels"
    id = Column(Integer, autoincrement=True, primary_key=True)
    s_label = Column(String(10), nullable=False)
    s_name = Column(String(20), nullable=False)
    s_background_color = Column(String(10), nullable=False, default="#fff")
    s_text_color = Column(String(10), nullable=False, default="#000")
    s_suffix_key = Column(String(5), comment="后缀")
    s_prefix_key = Column(String(5), comment="前缀")

    def to_config(self):
        return {
            "id": self.id,
            "text": self.s_label,
            "prefixKey": self.s_prefix_key,
            "suffixKey": self.s_suffix_key,
            "backgroundColor": self.s_background_color,
            "textColor": self.s_text_color,
        }
