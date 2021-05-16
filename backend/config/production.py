from config.baseconfig import ConfigBase
from config.secure import SecureInfo


class ProductionConfig(ConfigBase):
    # print('now in production mode')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = SecureInfo.get_mysql_of_production()
    MODE = "production"
