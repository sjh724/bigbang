import os


class config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret string'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/db_flask"


class TestingConfig(config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ""


class ProductionConfig(config):
    SQLALCHEMY_DATABASE_URI = ""


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
