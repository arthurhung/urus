class Config(object):
    DEBUG = True
    TESTING = False
    API_VERSION = "v1"


class IDC(Config):
    DEBUG = False
    DOMAIN = "128.110.24.97:5002"
    HTTPS_DOMAIN = "service.sinotrade.com.tw"


class UAT(Config):
    TESTING = True
    DOMAIN = "128.110.5.153:5002"
    HTTPS_DOMAIN = "servicerd.sinotrade.com.tw"
    SQLALCHEMY_DATABASE_URI = 'mysql://eyes:eyes147sino@218.32.237.72:3306/STG'


class Develop(Config):
    TESTING = True
    DOMAIN = "127.0.0.1:5000"
    SQLALCHEMY_DATABASE_URI = 'mysql://eyes:eyes147sino@218.32.237.72:3306/STG'