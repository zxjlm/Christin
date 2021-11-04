"""
@author: harumonia
@license: © Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: ner_api.py
@time: 2021/11/4 9:55 下午
@desc:
"""
from flask import Blueprint, render_template

from application.utils.normal import get_random_color

ner_api_bp = Blueprint("ner_api", __name__, url_prefix="/ner/api/v1")


@ner_api_bp.route('ner_visualization')
def ner_visualization_api():
    predict_result = {"annot": [{"start": 2, "end": 5, "ent": "time"}, {"start": 5, "end": 10, "ent": "ywyy"},
                                {"start": 12, "end": 22, "ent": "bczyzz"}, {"start": 23, "end": 27, "ent": "bczyzz"},
                                {"start": 28, "end": 35, "ent": "bczyzz"}, {"start": 36, "end": 43, "ent": "bczyzz"},
                                {"start": 44, "end": 47, "ent": "bczyzz"}, {"start": 48, "end": 50, "ent": "bczyzz"},
                                {"start": 51, "end": 54, "ent": "bczyzz"}, {"start": 55, "end": 60, "ent": "bczyzz"},
                                {"start": 61, "end": 64, "ent": "bczyzz"}, {"start": 65, "end": 67, "ent": "bczyzz"},
                                {"start": 68, "end": 74, "ent": "bczyzz"}, {"start": 75, "end": 80, "ent": "bczyzz"},
                                {"start": 81, "end": 83, "ent": "bczyzz"}, {"start": 88, "end": 90, "ent": "szks"},
                                {"start": 98, "end": 100, "ent": "szks"}, {"start": 102, "end": 105, "ent": "rycbzd"},
                                {"start": 116, "end": 118, "ent": "bcz"}, {"start": 119, "end": 122, "ent": "bcz"},
                                {"start": 123, "end": 128, "ent": "bcz"}],
                      "text": "患者1天前无明显诱因出现发作性头晕伴言语不清、口角歪斜，伴右下肢体麻木，时轻时重无头痛，无恶心、呕吐，无抽搐，"
                              "无意识不清，无心悸、胸闷，无大小便失禁，无视物旋转、模糊。随来我院门诊，为进一步诊治，门诊拟“TIA”收入住院。"
                              "病程中患者饮食、睡眠可，大小便正常。"}
    ents_ = sorted(predict_result['annot'], key=lambda x: x['start'])
    res = []
    left, right = 0, 0
    color_mapper = {foo['ent']: get_random_color() for foo in ents_}
    for ent in ents_:
        if ent['start'] >= right:
            res.append({'text': predict_result['text'][right: ent['start']], 'label': '%%'})
            left = ent['start']
            right = ent['end']
        res.append(
            {'text': predict_result['text'][left: right], 'label': ent['ent'], 'background': color_mapper[ent['ent']]})
    if right < len(predict_result['text']) - 1:
        res.append({'text': predict_result['text'][right:], 'label': '%%'})

    return render_template('ner/ner_visualization.html', render_list=res)
