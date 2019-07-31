# https://github.com/xen/flask-project-template
from flask import Flask
from .config import config_dict
import os
import locale
from .logger import log_err


def create_app():
    app = Flask(
        __name__,
        static_folder=None,
        template_folder=None)

    # cofigs = Prod | Azure(=Prod) | Dev | Lan
    config = os.environ.get('FLASK_CONFIG') or 'Prod'
    try:
        app.config.from_object(config_dict[config.capitalize()])
        app.logger.info('Usando config ' + config)
    except Exception as e:
        log_err(app, f'No se pudo cargar la configuración {config}.', e, False)

    # config mailer
    if app.config.get('SMTP_SEND_ERRORS'):
        app.config['_mailer_ok'] = False
        try:
            from .mailer import Mailer
            app._mailer = Mailer(app)
            app.logger.info('Usando Mailer')
            app.config['_mailer_ok'] = True
        except Exception as e:
            log_err(app, 'No se pudo crear el mailer.', e, False)
    else:
        app.logger.info('No usando Mailer')

    # configurar e inicializar scss
    if 'USE_SCSS' not in app.config:
        app.logger.warn('No se ha detectado el campo USE_SCSS en la configuración')
    else:
        if app.config['USE_SCSS']:
            try:
                create_scss_watch(app)
                app.logger.info('Usando SCSS')
            except Exception as e:
                log_err(app, 'No se pudo activar SCSS.', e, False)
        else:
            app.logger.info('No usando SCSS')

    # configurar e inicializar directus
    app.config['_directus_ok'] = False
    if 'USE_DIRECTUS' not in app.config:
        app.logger.warn('No se ha detectado el campo USE_DIRECTUS en la configuración')
    else:
        if app.config['USE_DIRECTUS']:
            try:
                import app.directus as directus
                directus.init_flask_app(app)
                app.logger.info('Usando Directus')
                app.config['_directus_ok'] = True
            except Exception as e:
                log_err(app, 'No se pudo activar Directus.', e, True)
        else:
            app.logger.info('No usando Directus')

    # chequear locale en español para que las fechas salgan en español y no en inglés
    try:
        config_locale(app)
    except Exception as e:
        log_err(app, 'No se pudo configurar la locale.', e, True)

    # config blueprints
    create_blueprints(app)

    return app


def create_blueprints(app):
    from .home import blueprint as home_bp
    app.register_blueprint(home_bp)


def create_scss_watch(app):
    from flask_scss import Scss
    Scss(
        app,
        static_dir=os.path.dirname(os.path.abspath(__file__))+'/home/static/css',
        asset_dir=os.path.dirname(os.path.abspath(__file__))+'/home/static/scss')


def config_locale(app):
    curr_lang = locale.getlocale()[0]

    if curr_lang[:2].lower() is 'es':
        loc_ok = True
    else:
        loc_ok = False
        try_locales = ['es_AR.utf8', 'es_ES.utf8', 'es.utf8']
        for loc in try_locales:
            try:
                locale.setlocale(locale.LC_TIME, loc)
                loc_ok = True
                break
            except locale.Error:
                continue

    if not loc_ok:
        log_err(app, 'No se encontró ningún locale en español en su sistema.', None, True)
