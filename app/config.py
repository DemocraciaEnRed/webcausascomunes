import os


class BaseConfig(object):
    USE_DIRECTUS = True
    DIRECTUS_API_PATH = '/api/1.1/'

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
    # SERVER_HOST = ''
    # SERVER_PORT = 0
    DEBUG = False
    SQLALCHEMY_ECHO = False
    USE_SCSS = False


class AzureConfig(ProductionConfig):
    DIRECTUS_URL_INTERNAL = os.environ.get('DIRECTUS_URL_INTERNAL')
    DIRECTUS_URL_EXTERNAL = os.environ.get('DIRECTUS_URL_EXTERNAL')
    DIRECTUS_TOKEN = os.environ.get('DIRECTUS_TOKEN')


class MoooConfig(ProductionConfig):
    DIRECTUS_URL_EXTERNAL = 'http://contenido.causascomunes.mooo.com/'
    DIRECTUS_URL_INTERNAL = 'http://192.168.0.92:9090'
    DIRECTUS_TOKEN = '4VIinWnI5zfyoJc5y69aBVyognPX0kpp'


# @@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@ DEBUG CONFIGS
class DevelopmentConfig(BaseConfig):
    SECRET_KEY = 'not a super secret key'
    SERVER_HOST = 'localhost'
    SERVER_PORT = 5000
    DEBUG = True
    SQLALCHEMY_ECHO = True
    USE_SCSS = True


class LocalConfig(DevelopmentConfig):
    DIRECTUS_URL_INTERNAL = 'http://localhost:9090'
    DIRECTUS_URL_EXTERNAL = 'http://localhost:9090'
    DIRECTUS_TOKEN = 'HUhmGTscM6tQv4KjK7NIlcsq5aklrcjM'


class CasaConfig(DevelopmentConfig):
    DIRECTUS_URL_INTERNAL = 'http://192.168.0.92:9090'
    DIRECTUS_URL_EXTERNAL = 'http://192.168.0.92:9090'
    DIRECTUS_TOKEN = '4VIinWnI5zfyoJc5y69aBVyognPX0kpp'


class RemoteConfig(DevelopmentConfig):
    DIRECTUS_URL_INTERNAL = 'http://contenido.causascomunes.mooo.com/'
    DIRECTUS_URL_EXTERNAL = 'http://contenido.causascomunes.mooo.com/'
    DIRECTUS_TOKEN = '4VIinWnI5zfyoJc5y69aBVyognPX0kpp'


config_dict = {
    # prod
    'Azure': AzureConfig,
    'Mooo': MoooConfig,
    # dev
    'Local': LocalConfig,
    'Casa': CasaConfig,
    'Remote': RemoteConfig
}
