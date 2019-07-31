import os


class BaseConfig(object):
    USE_DIRECTUS = True
    DIRECTUS_URL_INTERNAL = os.environ.get('DIRECTUS_URL_INTERNAL', '')
    DIRECTUS_URL_EXTERNAL = os.environ.get('DIRECTUS_URL_EXTERNAL', DIRECTUS_URL_INTERNAL)
    DIRECTUS_API_PATH = '/api/1.1/'
    DIRECTUS_TOKEN = os.environ.get('DIRECTUS_TOKEN', '')

    SMTP_SERVER = os.environ.get('SMTP_SERVER', '')
    SMTP_PORT = os.environ.get('SMTP_PORT', '')
    SMTP_USER = os.environ.get('SMTP_USER', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
    SMTP_TARGET_EMAIL = os.environ.get('SMTP_TARGET_EMAIL', '')


# @@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@ PROD CONFIGS
class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')

    USE_SCSS = False
    SMTP_SEND_ERRORS = os.environ.get('SMTP_SEND_ERRORS') or True


# @@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@ DEBUG CONFIGS
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dummy secret key'

    USE_SCSS = True
    SMTP_SEND_ERRORS = os.environ.get('SMTP_SEND_ERRORS') or False

    SERVER_HOST = 'localhost'
    SERVER_PORT = 5000


class LanConfig(DevelopmentConfig):
    SERVER_HOST = '192.168.88.20'


config_dict = {
    # prod
    'Prod': ProductionConfig,
    'Azure': ProductionConfig,
    # dev
    'Dev': DevelopmentConfig,
    'Lan': LanConfig,
}
