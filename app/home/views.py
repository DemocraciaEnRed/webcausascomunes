from flask import current_app, request, render_template, redirect, url_for, Blueprint
from pprint import pprint

blueprint = Blueprint(
    'home',
    __name__,
    url_prefix='/',
    static_folder="static",
    template_folder="templates")

accepted_causas = [
    'genero',
    'ambiente',
    'ciencia',
    'vivienda',
    'transparencia',
    'drogas',
    'trabajo'
]


def get_menu_navs():
    navs = {'index': '', 'causas': '', 'agenda': '', 'contacto': ''}
    endpoint = request.endpoint.split('.')[1]
    if endpoint in accepted_causas:
        navs['causas'] = 'active'
    elif endpoint in navs.keys():
        navs[endpoint] = 'active'
    return navs


@blueprint.after_request
def after_request(response):
    # para que el cliente pueda (solo) cargar las imágenes del dominio de directus
    response.headers['Access-Control-Allow-Origin'] = current_app.config['DIRECTUS_URL_EXTERNAL']
    return response


@blueprint.route("/", methods=['GET'])
def index():
    isstatic = False

    import app.directus as directus
    dimgsnav = directus.dapi.get_imgs_pagina('Navegacion')
    dimgsfooter = directus.dapi.get_imgs_pagina('Footer')
    dtextos = directus.dapi.get_textos_pagina('Home')
    dimgs = directus.dapi.get_imgs_pagina('Home')
    itemspropuestas = directus.dapi.get_items_propuestas()
    # itemsnovedades = directus.dapi.get_items_novedades('Home')
    itemsagenda = directus.dapi.get_items_agenda('Home')
    galeriahackaton = directus.dapi.get_galeria_hackaton()

    return render_template(
        'index.html',
        navs=get_menu_navs(),
        dimgsnav=dimgsnav,
        dimgsfooter=dimgsfooter,
        dtextos=dtextos,
        dimgs=dimgs,
        # itemsnovedades=itemsnovedades,
        itemsagenda=itemsagenda,
        itemspropuestas=itemspropuestas,
        galeriahackaton=galeriahackaton,
        isstatic=isstatic)


@blueprint.route("/contacto", methods=['GET'])
def contacto():
    isstatic = False

    import app.directus as directus
    dimgsnav = directus.dapi.get_imgs_pagina('Navegacion')
    dimgsfooter = directus.dapi.get_imgs_pagina('Footer')

    dtextos = directus.dapi.get_textos_pagina('Contacto')
    dimgs = directus.dapi.get_imgs_pagina('Contacto')

    return render_template(
        'contacto.html',
        navs=get_menu_navs(),
        dimgsnav=dimgsnav,
        dimgsfooter=dimgsfooter,
        dtextos=dtextos,
        dimgs=dimgs,
        isstatic=isstatic)


def causa(agenda):
    get_menu_navs()
    if agenda not in accepted_causas:
        return redirect(url_for('home.index'))

    isstatic = False

    import app.directus as directus

    dimgsnav = directus.dapi.get_imgs_pagina('Navegacion')
    dimgsfooter = directus.dapi.get_imgs_pagina('Footer')

    dtextos = directus.dapi.get_textos_pagina(agenda)
    dimgs = directus.dapi.get_imgs_pagina(agenda)

    itemstemas = directus.dapi.get_items_tema(agenda)
    itemsseguidores = directus.dapi.get_items_seguidor(agenda)
    itemsnovedades = directus.dapi.get_items_novedades(agenda)
    itemsagenda = directus.dapi.get_items_agenda(agenda)

    variables = {
        'navs': get_menu_navs(),
        'dimgsnav': dimgsnav,
        'dimgsfooter': dimgsfooter,

        'dtextos': dtextos,
        'dimgs': dimgs,

        'itemstemas': itemstemas,
        'itemsseguidores': itemsseguidores,
        'itemsnovedades': itemsnovedades,
        'itemsagenda': itemsagenda,

        'isstatic': isstatic}

    if agenda == 'sasdsd':
        variables['dtextosextra'] = {}
        variables['dimgsextra'] = {}

    return render_template('causa.html', **variables)


@blueprint.route("/genero", methods=['GET'])
def genero():
    return causa('genero')


@blueprint.route("/ambiente", methods=['GET'])
def ambiente():
    return causa('ambiente')


@blueprint.route("/ciencia", methods=['GET'])
def ciencia():
    return causa('ciencia')


@blueprint.route("/vivienda", methods=['GET'])
def vivienda():
    return causa('vivienda')


@blueprint.route("/drogas", methods=['GET'])
def drogas():
    return causa('drogas')


@blueprint.route("/trabajo", methods=['GET'])
def trabajo():
    return causa('trabajo')


@blueprint.route("/transparencia", methods=['GET'])
def transparencia():
    return causa('transparencia')


@blueprint.route("/trans", methods=['GET'])
def trans():
    isstatic = False

    import app.directus as directus
    dimgsnav = directus.dapi.get_imgs_pagina('Navegacion')
    dimgsfooter = directus.dapi.get_imgs_pagina('Footer')

    dtextos = directus.dapi.get_textos_pagina('Contacto')
    dimgs = directus.dapi.get_imgs_pagina('Contacto')

    import app.datos as datos
    # cols = datos.get_cols_from_csv(blueprint.static_folder + '/datos-presupuesto.csv')
    presu_heads = datos.get_presu_headers()
    presu_data = datos.get_rows_from_csv(blueprint.static_folder + '/datos-presupuesto.csv')

    return render_template(
        'transparencia.html',
        navs=get_menu_navs(),
        dimgsnav=dimgsnav,
        dimgsfooter=dimgsfooter,
        dtextos=dtextos,
        dimgs=dimgs,
        presu_heads=presu_heads,
        presu_data=presu_data,
        isstatic=isstatic)
