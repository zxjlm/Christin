from config.baseconfig import ConfigBase
from config.secure import SecureInfo


class TestingConfig(ConfigBase):
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = SecureInfo.get_mysql_of_test()
    SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}
    SECURITY_PASSWORD_HASH = "plaintext"
