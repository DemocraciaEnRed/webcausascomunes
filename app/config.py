class BaseConfig(object):
    SECRET_KEY = 'key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.dirname(os.path.abspath(__file__)) + '/db.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + INSTANCE_FOLDER_PATH + '/db.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://flask@127.0.0.1:3306/flaskdb?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123@127.0.0.1:3300/flaskdb?charset=utf8'
    DIRECTUS_URL = 'http://localhost:8080/'
    DIRECTUS_API_PATH = 'api/1.1/'
    DIRECTUS_TOKEN = '8sUdXIM5dd01rbeS7Z1H1mCJMILSTM26'
    USE_DIRECTUS = False
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
