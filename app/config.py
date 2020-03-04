import os


class BaseConfig(object):
    USE_DIRECTUS = True
    DIRECTUS_URL_INTERNAL = os.environ.get('DIRECTUS_URL_INTERNAL', '')
    DIRECTUS_URL_EXTERNAL = os.environ.get('DIRECTUS_URL_EXTERNAL', DIRECTUS_URL_INTERNAL)
    DIRECTUS_API_PATH = '/api/1.1/'
    DIRECTUS_TOKEN = os.environ.get('DIRECTUS_TOKEN', '')

    USE_SMTP = os.environ.get('USE_SMTP', '')
    SMTP_SERVER = os.environ.get('SMTP_SERVER', '')
    SMTP_PORT = os.environ.get('SMTP_PORT', '')
    SMTP_USER = os.environ.get('SMTP_USER', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
    SMTP_TARGET_EMAIL = os.environ.get('SMTP_TARGET_EMAIL', '')
    SMTP_TEST_ON_START = os.environ.get('SMTP_TEST_ON_START', '')

    USE_GSHEETS = os.environ.get('USE_GSHEETS', '')
    GSHEETS_CLIENT_ID = os.environ.get('GSHEETS_CLIENT_ID', '')
    GSHEETS_PROJECT_ID = os.environ.get('GSHEETS_PROJECT_ID', '')
    GSHEETS_CLIENT_SECRET = os.environ.get('GSHEETS_CLIENT_SECRET', '')
    GSHEETS_SHEET_ID = os.environ.get('GSHEETS_SHEET_ID', '')


# @@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@ PROD CONFIGS
class ProductionConfig(BaseConfig):
    #no anda debug así, settear la var de entorno FLASK_ENV=production
    #DEBUG = False
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')

    USE_SCSS = False


# @@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@ DEBUG CONFIGS
class DevelopmentConfig(BaseConfig):
    #no anda debug así, settear la var de entorno FLASK_ENV=development
    #DEBUG = True
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dummy secret key'

    USE_SCSS = True

    SERVER_HOST = '0.0.0.0'
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
