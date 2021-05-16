"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: apiconfig.py
@time: 2021/1/16 23:47
@desc:
"""


class ApiCode:
    def __init__(self):
        self.apiabort = ""
        self.apiwillabort = ""
        self.dataanalyzeunknownerror = ""
        self.downloaderror = ""
        self.forbidden = ""
        self.loginfailed = ""
        self.missingparameters = ""
        self.queryduplicate = ""
        self.querynone = ""
        self.repeatloginname = ""
        self.requesttypeerror = ""
        self.success = ""
        self.unauthorized = ""
        self.unknownerror = ""
        self.uploaddataerror = ""

    def init_app(self, appconfig):
        for k, v in appconfig.items():
            if k.startswith("CODE_"):
                key = k.replace("CODE_", "").lower()
                setattr(self, key, v)
