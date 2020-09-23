from flask import current_app, request, render_template, redirect, url_for, Blueprint
from datetime import datetime
from app.logger import log_err
import app.directus as directus

blueprint = Blueprint(
    'home',
    __name__,
    url_prefix='/',
    static_folder="static",
    template_folder="templates")

################
# En la última línea de este archivo se definen las rutas de las causas
################

accepted_causas = {
    'genero': 'Género',
    'ambiente': 'Ambiente',
    #'vivienda': 'Vivienda',
    'transparencia': 'Transparencia',
    'drogas': 'Drogas',
    'trabajo': 'Trabajo',
    'derechos-digitales': 'Derechos digitales'
}


def get_menu_navs():
    navs = {'index': '', 'causas': '', 'cuentas': '', 'colaboraciones': '', 'contacto': ''}
    if request.endpoint:
        endpoint = request.endpoint.split('.')[1] if '.' in request.endpoint else request.endpoint
        if endpoint in accepted_causas.keys():
            navs['causas'] = 'active'
        elif endpoint in navs.keys():
            navs[endpoint] = 'active'
    return navs


def render_error(msg):
    return render_template(
        "error.html",
        navs=get_menu_navs(),
        msg=msg,
        url='/')


########################### ERRORES
@blueprint.app_errorhandler(500)
def server_error(e):
    log_err(current_app, 'Server error 500.', e, True)

    if not request.endpoint or request.endpoint == 'home.index':
        msg = "¡Ups! La página no está funcionando correctamente<br>"\
               "El equipo técnico ya está trabajando para arreglarla<br>"\
               "Por favor, vuelva más tarde"
    else:
        msg = "¡Ups! Ha surgido un error<br>"\
               "Por favor, regrese a la <a href='/'>página principal</a> y vuelva a internarlo"

    return render_error(msg)


@blueprint.app_errorhandler(404)
def not_found(e):
    msg = "No encontramos la página que está buscando<br>"\
          "Por favor, verifique que la dirección esté bien escrita o vuelva a la <a href='/'>página principal</a>"
    return render_error(msg)


@blueprint.before_request
def before_request():
    # si no está activo directus cancelamos la request, pero si es a un recurso estático la dejamos pasar
    #if request.endpoint != 'home.index':
    if not current_app.config['_using_directus'] and 'static' not in request.endpoint and 'home.' in request.endpoint:
        log_err(current_app, 'Directus in error state.', None, True)

        msg = "La página se encuentra en mantenimiento<br>"\
              "Por favor, vuelva en otro momento"
        return render_error(msg)


@blueprint.after_request
def after_request(response):
    # para que el cliente pueda (solo) cargar las imágenes del dominio de directus
    if current_app.config['_using_directus']:
        response.headers['Access-Control-Allow-Origin'] = current_app.config['DIRECTUS_URL_EXTERNAL']
    return response


@blueprint.route("/", methods=['GET'])
def index():
    if current_app.config['_using_directus']:
        import app.directus as directus
        dtextos = directus.dapi.get_textos_pagina('Home')
        dimgs = directus.dapi.get_imgs_pagina('Home')
        itemspropuestas = directus.dapi.get_items_propuestas()
        #itemsagenda = directus.dapi.get_items_agenda('Home')
    else:
        import app.content as content
        dtextos = content.textos_home()
        dimgs = {}
        itemspropuestas = content.items_propuestas()
        #itemsagenda = {}


    return render_template(
        'index.html',
        navs = get_menu_navs(),
        dtextos = dtextos,
        dimgs = dimgs,
        #itemsagenda = itemsagenda,
        itemspropuestas = itemspropuestas,
        index_de_testeo='indexDeTesteo' in request.endpoint)


@blueprint.route("/contacto", methods=['GET'])
def contacto():
    return render_template(
        'contacto.html',
        navs = get_menu_navs(),
        dtextos = directus.dapi.get_textos_pagina('Contacto'),
        dimgs = directus.dapi.get_imgs_pagina('Contacto'))


def _get_causa_from_endpoint():
    split = request.endpoint.split('.')
    if len(split) < 2:
        return None

    causa = request.endpoint.split('.')[1]
    # a algunos endpoints (como el de scrollys) le ponemos "_" en el nombre, después del nombre de la causa
    causa = causa.split('_')[0]
    if causa not in accepted_causas.keys():
        return None

    return causa


def causas_route():
    causa = _get_causa_from_endpoint()
    if causa is None:
        return redirect(url_for('home.index'))

    import app.directus as directus

    dtextoscausas = directus.dapi.get_textos_pagina('Causas')
    dtextos = directus.dapi.get_textos_pagina(causa)
    dimgs = directus.dapi.get_imgs_pagina(causa)
    itemsscrolly = directus.dapi.get_items_scrolly(causa)
    dmapa = directus.dapi.get_item_mapa(causa)

    #itemstemas = directus.dapi.get_items_tema(causa)
    #itemsagenda = directus.dapi.get_items_agenda(causa)
    #itemscompromisos = directus.dapi.get_items_compromisos(causa)

    causas_names = list(accepted_causas.keys())
    current_causa_i = causas_names.index(causa)

    if current_causa_i == 0:
        causa_prev = causas_names[-1]
        causa_next = causas_names[current_causa_i + 1]
    elif current_causa_i == len(causas_names) - 1:
        causa_prev = causas_names[current_causa_i - 1]
        causa_next = causas_names[0]
    else:
        causa_prev = causas_names[current_causa_i - 1]
        causa_next = causas_names[current_causa_i + 1]

    causa_prev_tit = accepted_causas[causa_prev]
    causa_next_tit = accepted_causas[causa_next]

    variables = {
        'navs': get_menu_navs(),

        'dtextoscausas': dtextoscausas,
        'dtextos': dtextos,
        'dimgs': dimgs,

        #'itemstemas': itemstemas,
        #'itemsagenda': itemsagenda,
        #'itemscompromisos': itemscompromisos,

        'show_wiki_btn': True,
        'causa': causa,
        'causa_prev': causa_prev,
        'causa_prev_tit': causa_prev_tit,
        'causa_next': causa_next,
        'causa_next_tit': causa_next_tit,
        'nombre_causa': accepted_causas[causa],
        'itemsscrolly': itemsscrolly,
        'dmapa': dmapa
    }

    return render_template('causa.html', **variables)


@blueprint.route("/cuentas", methods=['GET'])
def cuentas():
    import app.directus as directus
    dimgsnav = directus.dapi.get_imgs_pagina('Navegacion')
    dimgsfooter = directus.dapi.get_imgs_pagina('Footer')

    dtextos = directus.dapi.get_textos_pagina('Cuentas')

    from app.datos import Cuentas
    dataset_cuentas = Cuentas(blueprint.static_folder + '/datos-presupuesto.csv')
    dataset_headers = dataset_cuentas.get_rendered_headers()

    # if current_app._gsheetapi:
    if False:
        dataset_rows = dataset_cuentas.get_rows_from_gsheet(current_app._gsheetapi)
    else:
        # cols = datos.get_cols_from_csv(blueprint.static_folder + '/datos-presupuesto.csv')
        dataset_rows = dataset_cuentas.get_rows_from_csv()

    fechas_epoch = []
    fecha_i = dataset_headers.index('fecha')
    for row in dataset_rows:
        try:
            date = datetime.strptime(row[fecha_i], '%d/%m/%Y')
            date = date.strftime('%s')
        except:
            date = ''
        fechas_epoch.append(date)

    dataset_headers = [h.capitalize() for h in dataset_headers]

    return render_template(
        'transparencia.html',
        navs=get_menu_navs(),
        dimgsnav=dimgsnav,
        dimgsfooter=dimgsfooter,
        dtextos=dtextos,
        presu_heads=dataset_headers,
        presu_data=dataset_rows,
        fechas_epoch=fechas_epoch)



@blueprint.route("/colaboraciones", methods=['GET'])
def colaboraciones():
    import app.directus as directus
    dimgsnav = directus.dapi.get_imgs_pagina('Navegacion')
    dimgsfooter = directus.dapi.get_imgs_pagina('Footer')

    dtextos = directus.dapi.get_textos_pagina('Colaboraciones')

    from app.datos import Colaboraciones
    dataset_colaboraciones = Colaboraciones(blueprint.static_folder + '/CC_contabilidad_tiempo - Sheet1.csv')
    dataset_headers = dataset_colaboraciones.get_rendered_headers()

    # if current_app._gsheetapi:
    if False:
        dataset_rows = dataset_colaboraciones.get_rows_from_gsheet(current_app._gsheetapi)
    else:
        # cols = datos.get_cols_from_csv(blueprint.static_folder + '/datos-presupuesto.csv')
        dataset_rows = dataset_colaboraciones.get_rows_from_csv()

    # me guardo los aportantes y formateo las fechas
    aportantes = []
    aportantes_i = dataset_headers.index('aportante')
    fechas_epoch = []
    fecha_i = dataset_headers.index('fecha')
    for row in dataset_rows:
        if row[aportantes_i] and row[aportantes_i] not in aportantes:
            aportantes.append(row[aportantes_i])

        try:
            date = datetime.strptime(row[fecha_i], '%B')
            date = date.strftime('%s')
        except:
            date = ''
        fechas_epoch.append(date)

    # capitalizo los headers
    dataset_headers = [h.capitalize() for h in dataset_headers if h != 'aportante']

    # saco los aportantes del dataset
    dataset_rows_anon = []
    for row in dataset_rows:
        if aportantes_i < len(row):
            del row[aportantes_i]
        dataset_rows_anon.append(row)
    dataset_rows = None

    return render_template(
        'colaboraciones.html',
        navs=get_menu_navs(),
        dimgsnav=dimgsnav,
        dimgsfooter=dimgsfooter,
        dtextos=dtextos,
        aportantes=aportantes,
        presu_heads=dataset_headers,
        presu_data=dataset_rows_anon,
        fechas_epoch=fechas_epoch)



for causa in accepted_causas.keys():
    blueprint.add_url_rule(f'/{causa}', endpoint=causa, view_func=causas_route)

blueprint.add_url_rule(f'/indexDeTesteo', endpoint='indexDeTesteo', view_func=index)
