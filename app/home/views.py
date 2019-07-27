from flask import current_app, g, request, render_template, redirect, url_for, Blueprint
from app.app import using_directus

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
    try:
        endpoint = request.endpoint.split('.')[1]
        if endpoint in accepted_causas:
            navs['causas'] = 'active'
        elif endpoint in navs.keys():
            navs[endpoint] = 'active'
    except Exception as e:
        current_app.logger.error('No se pudo configurar el menú de navegación. ' + str(e))
    return navs


@blueprint.before_request
def before_request():
    g.isstatic = not using_directus
    print(g.using_directus)


@blueprint.after_request
def after_request(response):
    # para que el cliente pueda solo cargar las imágenes del dominio de directus
    if current_app.config['DIRECTUS_URL_EXTERNAL']:
        response.headers['Access-Control-Allow-Origin'] = current_app.config['DIRECTUS_URL_EXTERNAL']
    return response


@blueprint.route("/", methods=['GET'])
def index():
    if g.isstatic:
        dimgsnav = {}
        dimgsfooter = {}

        dtextos = {}
        dimgs = {}

        itemspropuestas = {}
        # itemsnovedades = {}
        itemsagenda = {}
        galeriahackaton = {}
    else:
        from app.directus import dapi

        dimgsnav = dapi.get_imgs_pagina('Navegacion')
        dimgsfooter = dapi.get_imgs_pagina('Footer')

        dtextos = dapi.get_textos_pagina('Home')
        dimgs = dapi.get_imgs_pagina('Home')

        itemspropuestas = dapi.get_items_propuestas()
        # itemsnovedades = dapi.get_items_novedades('Home')
        itemsagenda = dapi.get_items_agenda('Home')
        galeriahackaton = dapi.get_items_hackaton()

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
        isstatic=g.isstatic)


@blueprint.route("/contacto", methods=['GET'])
def contacto():
    if g.isstatic:
        dimgsnav = {}
        dimgsfooter = {}

        dtextos = {}
        dimgs = {}
    else:
        from app.directus import dapi

        dimgsnav = dapi.get_imgs_pagina('Navegacion')
        dimgsfooter = dapi.get_imgs_pagina('Footer')

        dtextos = dapi.get_textos_pagina('Contacto')
        dimgs = dapi.get_imgs_pagina('Contacto')

    return render_template(
        'contacto.html',
        navs=get_menu_navs(),
        dimgsnav=dimgsnav,
        dimgsfooter=dimgsfooter,
        dtextos=dtextos,
        dimgs=dimgs,
        isstatic=g.isstatic)


def causa(agenda):
    if agenda not in accepted_causas:
        return redirect(url_for('home.index'))

    if g.isstatic:
        dimgsnav = {}
        dimgsfooter = {}

        dtextos = {}
        dimgs = {}

        itemstemas = {}
        itemsseguidores = {}
        itemsnovedades = {}
        itemsagenda = {}
    else:
        from app.directus import dapi

        dimgsnav = dapi.get_imgs_pagina('Navegacion')
        dimgsfooter = dapi.get_imgs_pagina('Footer')

        dtextos = dapi.get_textos_pagina(agenda)
        dimgs = dapi.get_imgs_pagina(agenda)

        itemstemas = dapi.get_items_tema(agenda)
        itemsseguidores = dapi.get_items_seguidor(agenda)
        itemsnovedades = dapi.get_items_novedades(agenda)
        itemsagenda = dapi.get_items_agenda(agenda)

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
        'isstatic': g.isstatic}

    # dejo la ventana abierta por si algún día queremos mandar cosas específicas por causas
    '''if agenda == 'sasdsd':
        variables['dtextosextra'] = {}
        variables['dimgsextra'] = {}'''

    return render_template('causa.html', **variables)


# rutas para las 7 causas, método a mejorar
@blueprint.route("/genero", methods=['GET'])
def genero(): return causa('genero')
@blueprint.route("/ambiente", methods=['GET'])
def ambiente(): return causa('ambiente')
@blueprint.route("/ciencia", methods=['GET'])
def ciencia(): return causa('ciencia')
@blueprint.route("/vivienda", methods=['GET'])
def vivienda(): return causa('vivienda')
@blueprint.route("/drogas", methods=['GET'])
def drogas(): return causa('drogas')
@blueprint.route("/trabajo", methods=['GET'])
def trabajo(): return causa('trabajo')
@blueprint.route("/transparencia", methods=['GET'])
def transparencia(): return causa('transparencia')
