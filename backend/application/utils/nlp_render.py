"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: nlp_render.py
@time: 2021/1/10 12:00
@desc: nlp渲染
"""
from spacy import Errors
from spacy.displacy import DependencyRenderer, parse_deps, parse_ents, EntityRenderer
from spacy.tokens.doc import Doc
from spacy.tokens.span import Span

from application.models import Labels


def my_json_render(docs, style="dep", options=None, manual=False) -> list:
    """
    Render nlp visualisation.
    Args:
        docs (list or Doc): Document(s) to visualise.
        style (unicode): Visualisation style, 'dep' or 'ent'.
        options (dict): Visualiser-specific options, e.g. colors.
        manual (bool): Don't parse `Doc` and
                        instead expect a dict/list of dicts.

    Returns:
        [{'text': '近一周饮食不当,一度腹泻,日3次,泻下后精神疲烦,时有低热,怕风,口干,痰中夹有血丝,左侧胸痛时作',
        'ents': [{'start': 20, 'end': 24, 'label': 'ZZ'},
        {'start': 25, 'end': 27, 'label': 'CD'},
        {'start': 27, 'end': 29, 'label': 'ZZ'},
        {'start': 30, 'end': 32, 'label': 'ZZ'},
        {'start': 33, 'end': 35, 'label': 'ZZ'},
        {'start': 36, 'end': 42, 'label': 'ZZ'}],
        'title': None, 'settings': {'lang': 'zh', 'direction': 'ltr'}}]
    """

    if options is None:
        options = {}
    factories = {
        "dep": (DependencyRenderer, parse_deps),
        "ent": (EntityRenderer, parse_ents),
    }
    if style not in factories:
        raise ValueError(Errors.E087.format(style=style))
    if isinstance(docs, (Doc, Span, dict)):
        docs = [docs]
    docs = [obj if not isinstance(obj, Span) else obj.as_doc() for obj in docs]
    if not all(isinstance(obj, (Doc, Span, dict)) for obj in docs):
        raise ValueError(Errors.E096)
    renderer, converter = factories[style]
    renderer = renderer(options=options)
    parsed = [converter(doc, options) for doc in docs] if not manual else docs
    return parsed


def doccano_wapper(results: list):
    """
    将 spacy 的分类结果转变为符合doccano标注风格的结果
    Args:
        results:

    Returns:

    """
    labels = [foo.to_config() for foo in Labels.query.all()]
    label_mapper = {label["text"]: label["id"] for label in labels}
    count = 0
    ret = []
    for result in results:
        tmp = []
        for ent in result["ents"]:
            tmp.append(
                {
                    "id": count,
                    "label": label_mapper[ent["label"]],
                    "startOffset": ent["start"],
                    "endOffset": ent["end"],
                }
            )
            count += 1
        ret.append({"text": result["text"], "annotations": tmp})
    return {"nerDocs": ret, "labels": labels}
