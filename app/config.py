import os


class BaseConfig(object):
    SERVER_HOST = 'localhost'
    SERVER_PORT = 5000

    USE_DIRECTUS = True
    DIRECTUS_API_PATH = '/api/1.1/'
    DIRECTUS_TOKEN = os.environ.get('DIRECTUS_TOKEN') or ''

    SMTP_SEND_ERRORS = os.environ.get('SMTP_SEND_ERRORS') or ''
    SMTP_SERVER = os.environ.get('SMTP_SERVER') or ''
    SMTP_PORT = os.environ.get('SMTP_PORT') or ''
    SMTP_USER = os.environ.get('SMTP_USER') or ''
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD') or ''
    SMTP_TARGET_EMAIL = os.environ.get('SMTP_TARGET_EMAIL') or ''

    # USE_EXTENSIONS = False
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.dirname(os.path.abspath(__file__)) + '/db.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + INSTANCE_FOLDER_PATH + '/db.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://flask@127.0.0.1:3306/flaskdb?charset=utf8'
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123@127.0.0.1:3300/flaskdb?charset=utf8'


# @@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@ PROD CONFIGS
class ProductionConfig(BaseConfig):
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'jKdy5629ddJk change me please'
    DEBUG = False
    SQLALCHEMY_ECHO = False
    USE_SCSS = False


class AzureConfig(ProductionConfig):
    DIRECTUS_URL_INTERNAL = os.environ.get('DIRECTUS_URL_INTERNAL') or ''
    DIRECTUS_URL_EXTERNAL = os.environ.get('DIRECTUS_URL_EXTERNAL') or ''


class MoooConfig(ProductionConfig):
    DIRECTUS_URL_EXTERNAL = 'http://contenido.causascomunes.mooo.com/'
    DIRECTUS_URL_INTERNAL = 'http://192.168.0.92:9090'


# @@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@ DEBUG CONFIGS
class DevelopmentConfig(BaseConfig):
    SECRET_KEY = 'not a super secret key'
    DEBUG = True
    SQLALCHEMY_ECHO = True
    USE_SCSS = True


class LocalConfig(DevelopmentConfig):
    DIRECTUS_URL_INTERNAL = 'http://localhost:9090'
    DIRECTUS_URL_EXTERNAL = 'http://localhost:9090'


class DerConfig(DevelopmentConfig):
    DIRECTUS_URL_INTERNAL = 'https://directus.democraciaenred.org/'
    DIRECTUS_URL_EXTERNAL = 'https://directus.democraciaenred.org/'


config_dict = {
    # prod
    'Azure': AzureConfig,
    'Mooo': MoooConfig,
    # dev
    'Local': LocalConfig,
    'Der': DerConfig
}
