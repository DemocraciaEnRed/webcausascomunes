# https://github.com/xen/flask-project-template
from flask import Flask
import os
import locale
from .logger import log_err
from logging import INFO


def _check_config_field(app, field):
    if field not in app.config:
        app.logger.warn(f'No se ha detectado el campo {field} en la configuración')
        return False
    else:
        return True


def _config_is_true(env):
    return str(env).lower() not in ['no', 'false', '0']

def _root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(
        __name__,
        static_folder=None,
        template_folder=None)
    app.logger.setLevel(INFO)

    # configurar e inicializar env
    if os.environ.get('LOAD_ENV'):
        from dotenv import load_dotenv
        from os.path import join, dirname, isfile
        from os import environ
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        app.logger.info('Usando .env')
    else:
        app.logger.info('No usando .env')

    # cofigs = Prod | Azure(=Prod) | Dev | Lan
    from .config import config_dict
    config = os.environ.get('FLASK_CONFIG') or 'Prod'
    try:
        app.config.from_object(config_dict[config.capitalize()])
        app.logger.info('Usando config ' + config)
    except Exception as e:
        log_err(app, f'No se pudo cargar la configuración {config}.', e, False)

    def _extension_loader(config_field, extension_name, flag_name=None):
        def real_decorator(extension_loader):
            def wrapper(*args, **kwargs):
                if flag_name:
                    app.config[flag_name] = False
                if config_field not in app.config:
                    log_err(app, f'No se ha detectado el campo {config_field} en la configuración.'
                            f'Extensión {extension_name} desactivada.', None, False)
                else:
                    if _config_is_true(app.config.get(config_field, '')):
                        try:
                            extension_loader(*args, **kwargs)
                        except Exception as e:
                            log_err(app, f'No se pudo activar la extensión {extension_name}.', e, False)
                        else:
                            app.logger.info(f'Extensión {extension_name} cargada')
                            if flag_name:
                                app.config[flag_name] = True
                    else:
                        app.logger.info(f'Extensión {extension_name} desactivada')

            return wrapper
        return real_decorator

    @_extension_loader("USE_SMTP", "Mailer", "_using_mailer")
    def load_mailer():
        from app.mailer import Mailer
        app._mailer = Mailer(app)
        if _config_is_true(app.config.get('SMTP_TEST_ON_START', '')):
            app._mailer.send_mail('Mail de prueba de web de causas comunes', 'Hola 123')
            app.logger.info(f'Mail de prueba enviado')

    @_extension_loader("USE_SCSS", "SCSS")
    def load_scss():
        from flask_scss import Scss
        Scss(
            app,
            static_dir=os.path.dirname(os.path.abspath(__file__))+'/home/static/css',
            asset_dir=os.path.dirname(os.path.abspath(__file__))+'/home/static/scss')

    @_extension_loader("USE_DIRECTUS", "Directus", "_using_directus")
    def load_directus():
        import app.directus as directus
        directus.init_flask_app(app)

    @_extension_loader("USE_GSHEETS", "Google Sheets", "_using_gsheets")
    def load_google_sheets():
        from app.google_sheets import GSheetApi
        app._gsheetapi = GSheetApi(app)

    load_mailer()
    load_scss()
    load_directus()
    load_google_sheets()

    # chequear locale en español para que las fechas salgan en español y no en inglés
    try:
        config_locale(app)
    except Exception as e:
        log_err(app, 'No se pudo configurar la locale.', e, True)

    # config blueprints
    create_blueprints(app)

    @app.context_processor
    def utility_processor():
        def print_svg(svg_filename):
            #print(svg_filename, dir(app))

            svg_cont = ''
            with open(_root_dir() + '/home/static/' + svg_filename) as f:
                svg_cont = f.read()
            return svg_cont
        return dict(print_svg=print_svg)

    return app


def create_blueprints(app):
    from .home import blueprint as home_bp
    app.register_blueprint(home_bp)


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
