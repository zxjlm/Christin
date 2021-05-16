from config.secure import SecureInfo


class ConfigBase:
    SECRET_KEY = "AAAAC3NzaC1lZDI1NTE5AAAAIMg+50AdolCristink357HclH++CBomDIBO"

    # BABEL_DEFAULT_LOCALE = 'zh'

    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = 25
    MAIL_USERNAME = SecureInfo.get_mail_user()
    MAIL_PASSWORD = SecureInfo.get_mail_passwd()
    MAIL_DEFAULT_SENDER = SecureInfo.get_mail_user()

    SQLALCHEMY_DATABASE_URI = SecureInfo.get_mysql_of_development()
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False

    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

    SECURITY_PASSWORD_SALT = "265350013214290708567714936437495833186"
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_DEFAULT_REMEMBER_ME = True
    SECURITY_TRACKABLE = True

    # no forms so no concept of flashing
    SECURITY_FLASH_MESSAGES = False

    # Need to be able to route backend flask API calls. Use 'accounts'
    # to be the Flask-Security endpoints.
    SECURITY_URL_PREFIX = "/api/accounts"

    # Turn on all the great Flask-Security features
    SECURITY_RECOVERABLE = True
    # SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True
    # SECURITY_CONFIRMABLE = True
    # SECURITY_REGISTERABLE = True
    # SECURITY_UNIFIED_SIGNIN = True
    # SECURITY_US_ENABLED_METHODS = [
    #     {"email": {"mapper": uia_email_mapper, "case_insensitive": True}},
    #     {"us_phone_number": {"mapper": uia_phone_mapper}},
    # ]

    # These need to be defined to handle redirects
    # As defined in the API documentation - they will receive the relevant context
    SECURITY_POST_CONFIRM_VIEW = "/confirmed"
    SECURITY_CONFIRM_ERROR_VIEW = "/confirm-error"
    SECURITY_RESET_VIEW = "/reset-password"
    SECURITY_RESET_ERROR_VIEW = "/reset-password"
    SECURITY_REDIRECT_BEHAVIOR = "spa"

    # CSRF protection is critical for all session-based browser UIs

    # enforce CSRF protection for session / browser - but allow token-based
    # API calls to go through
    # SECURITY_CSRF_PROTECT_MECHANISMS = ["session", "basic"]
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True

    # Send Cookie with csrf-token. This is the default for Axios and Angular.
    SECURITY_CSRF_COOKIE = {"key": "XSRF-TOKEN"}
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_TIME_LIMIT = None

    NEO4J_CONFIG = SecureInfo.get_neo4j_config()

    JSON_SORT_KEYS = False
    JSON_AS_ASCII = False

    # BABEL_TRANSLATION_DIRECTORIES = "./application/translations"

    # SWAGGER = {
    #     "title": "Flasgger Parsed Method/Function View Example",
    #     "doc_dir": "./swagger_files/",
    # }

    CODE_SUCCESS = {"code": "2000", "zhmsg": "成功", "enmsg": "Success", "data": "应有的数据"}
    CODE_FORBIDDEN = {
        "code": "2002",
        "zhmsg": "用户权限不足",
        "enmsg": "Forbidden",
        "data": "None",
    }
    CODE_UNAUTHORIZED = {
        "code": "2003",
        "zhmsg": "未认证的用户",
        "enmsg": "Unauthorized",
        "data": "None",
    }
    CODE_REPEATLOGINNAME = {
        "code": "2004",
        "zhmsg": "登录名已被占用",
        "enmsg": "RepeatLoginname",
        "data": "None",
    }
    CODE_LOGINFAILED = {
        "code": "2005",
        "zhmsg": "登录失败，检查登录名或者密码",
        "enmsg": "LoginnameOrPasswordError",
        "data": "None",
    }
    CODE_REQUESTTYPEERROR = {
        "code": "4001",
        "zhmsg": "请求参数类型错误",
        "enmsg": "RequestTypeError",
        "data": "None",
    }
    CODE_MISSINGPARAMETERS = {
        "code": "4002",
        "zhmsg": "缺少必要的参数",
        "enmsg": "MissingParameters",
        "data": "None",
    }
    CODE_UPLOADDATAERROR = {
        "code": "4003",
        "zhmsg": "上传的数据有误",
        "enmsg": "UploadDataError",
        "data": "None",
    }
    CODE_APIWILLABORT = {
        "code": "5000",
        "zhmsg": "请求成功，但是该api即将停止服务",
        "enmsg": "ApiWillAbort",
        "data": "None",
    }
    CODE_DATAANALYZEUNKNOWNERROR = {
        "code": "5001",
        "zhmsg": "分析内容出错，原因未知",
        "enmsg": "DataAnalyzeUnknownError",
        "data": "Expection",
    }
    CODE_APIABORT = {
        "code": "5005",
        "zhmsg": "api已经停止使用",
        "enmsg": "ApiAbort",
        "data": "None",
    }
    CODE_DOWNLOADERROR = {
        "code": "5006",
        "zhmsg": "下载失败",
        "enmsg": "DownloadError",
        "data": "None",
    }
    CODE_UNKNOWNERROR = {
        "code": "6001",
        "zhmsg": "请求失败,原因未知",
        "enmsg": "UnknownError",
        "data": "None",
    }
    CODE_QUERYNONE = {
        "code": "6007",
        "zhmsg": "查无此物",
        "enmsg": "QueryNone",
        "data": "None",
    }
    CODE_QUERYDUPLICATE = {
        "code": "6008",
        "zhmsg": "药名重复",
        "enmsg": "QueryDuplicate",
        "data": "None",
    }
