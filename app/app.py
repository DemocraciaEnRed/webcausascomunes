# https://github.com/xen/flask-project-template
from flask import Flask
from .config import config_dict
import os
import locale


def create_app():
    print('Creating flask app')
    app = Flask(
        __name__,
        static_folder=None,
        template_folder=None)

    app.config.from_object(config_dict['Debug'])

    create_logger(app)
    create_blueprints(app)
    if app.config['USE_SCSS']:
        create_scss_watch(app)
    # if app.config['USE_EXTENSIONS']:
    #     create_extensions(app)
    if app.config['USE_DIRECTUS']:
        import app.directus as directus
        directus.init_flask_app(app.config['DIRECTUS_URL_INTERNAL'], app.config['DIRECTUS_URL_EXTERNAL'], app.config['DIRECTUS_API_PATH'], app.config['DIRECTUS_TOKEN'])

    # chequear locale en español para que las fechas salga en español y no en inglés
    curr_lang = locale.getlocale()[0]
    if curr_lang[:2].lower() is not 'es':
        try:
            locale.setlocale(locale.LC_TIME, 'es_AR.utf8')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
            except locale.Error:
                try:
                    locale.setlocale(locale.LC_TIME, 'es.utf8')
                except locale.Error:
                    raise Exception('No se encontró ningún idioma español válido en su sistema.')

    return app


def create_logger(app):
    pass


def create_blueprints(app):
    from .home import blueprint as home_bp
    app.register_blueprint(home_bp)


def create_scss_watch(app):
    from flask_scss import Scss
    Scss(
        app,
        static_dir=os.path.dirname(os.path.abspath(__file__))+'/home/static/css',
        asset_dir=os.path.dirname(os.path.abspath(__file__))+'/home/static/scss')


def create_extensions(app):
    from .extensions import db
    db.init_app(app)

    from .extensions import login_manager
    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(id)
    login_manager.login_view = 'frontend.login'
    login_manager.init_app(app)
