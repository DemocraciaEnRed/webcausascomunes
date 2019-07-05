import os
print(os.environ)

class BaseConfig(object):
    SECRET_KEY = 'key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.dirname(os.path.abspath(__file__)) + '/db.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + INSTANCE_FOLDER_PATH + '/db.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://flask@127.0.0.1:3306/flaskdb?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123@127.0.0.1:3300/flaskdb?charset=utf8'
    DIRECTUS_URL = 'http://192.168.88.20:9090'
    # DIRECTUS_URL = 'http://directus:8080'
    DIRECTUS_API_PATH = '/api/1.1/'
    DIRECTUS_TOKEN = 'l5mMXIMYEUpfefI8AQkRA8sSHURn5Yvs'
    USE_DIRECTUS = False
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
