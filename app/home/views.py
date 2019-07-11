from flask import current_app, request, render_template, redirect, url_for, Blueprint

blueprint = Blueprint(
    'home',
    __name__,
    url_prefix='/',
    static_folder="static",
    template_folder="templates")


@blueprint.route("/", methods=['GET'])
def index():
    isstatic = not current_app.config['USE_DIRECTUS']
    if isstatic:
        import app.directus_fake as directus_fake
        dtextos = directus_fake.get_index_textos()
        dimgs = directus_fake.get_index_imgs()
        itemsnovedades = directus_fake.get_novedades_items()
        itemsagenda = directus_fake.get_agenda_items()
        itemspropuestas = directus_fake.get_propuesta_items()
        dimgsfooter = directus_fake.get_footer_imgs()
    else:
        import app.directus as directus
        dimgsnav = directus.dapi.get_imgs_pagina('Navegacion')
        dimgsfooter = directus.dapi.get_imgs_pagina('Footer')
        dtextos = directus.dapi.get_textos_pagina('Home')
        dimgs = directus.dapi.get_imgs_pagina('Home')
        itemspropuestas = directus.dapi.get_items_propuestas()
        itemsnovedades = directus.dapi.get_items_novedades('Home')
        itemsagenda = directus.dapi.get_items_agenda('Home')
    return render_template(
        'index.html',
        dimgsnav=dimgsnav,
        dimgsfooter=dimgsfooter,
        dtextos=dtextos,
        dimgs=dimgs,
        itemsnovedades=itemsnovedades,
        itemsagenda=itemsagenda,
        itemspropuestas=itemspropuestas,
        isstatic=isstatic)


def causa(agenda):
    accepted_causas = [
        'genero',
        'ambiente',
        'ciencia',
        'vivienda',
        'transparencia',
        'drogas',
        'trabajo'
    ]
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
