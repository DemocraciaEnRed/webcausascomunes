import os


class BaseConfig(object):
    SECRET_KEY = 'key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.dirname(os.path.abspath(__file__)) + '/db.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + INSTANCE_FOLDER_PATH + '/db.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://flask@127.0.0.1:3306/flaskdb?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123@127.0.0.1:3300/flaskdb?charset=utf8'
    # DIRECTUS_URL_EXTERNAL = 'http://causascomunes.mooo.com/images'
    DIRECTUS_URL_EXTERNAL = os.environ.get('DIRECTUS_URL_EXTERNAL') or 'http://localhost:9090'
    DIRECTUS_URL_INTERNAL = os.environ.get('DIRECTUS_URL_INTERNAL') or 'http://localhost:9090'
    # DIRECTUS_URL_EXTERNAL = 'http://192.168.0.92:9090'
    # DIRECTUS_URL_INTERNAL = 'http://192.168.0.92:9090'
    # DIRECTUS_URL_EXTERNAL = 'http://localhost:9090'
    DIRECTUS_API_PATH = '/api/1.1/'
    # DIRECTUS_TOKEN = '4VIinWnI5zfyoJc5y69aBVyognPX0kpp'
    DIRECTUS_TOKEN = os.environ.get('DIRECTUS_TOKEN') or 'HUhmGTscM6tQv4KjK7NIlcsq5aklrcjM'
    USE_DIRECTUS = True
    USE_SCSS = True
    USE_EXTENSIONS = False
    # SERVER_HOST = '192.168.88.20'
    SERVER_HOST = 'localhost'
    SERVER_PORT = 5000


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_ECHO = False


class DebugConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
