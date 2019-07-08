from flask import current_app, render_template, Blueprint

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
        dtextos = directus.dapi.get_textos_pagina('Home')
        dimgs = directus.dapi.get_imgs_pagina('Home')
        itemsnovedades = directus.dapi.get_items_novedades()
        itemsagenda = directus.dapi.get_items_agenda()
        itemspropuestas = directus.dapi.get_items_propuestas()
        dimgsfooter = directus.dapi.get_imgs_pagina('Footer')
    return render_template(
        'index.html',
        dtextos=dtextos,
        dimgs=dimgs,
        dimgsfooter=dimgsfooter,
        itemsnovedades=itemsnovedades,
        itemsagenda=itemsagenda,
        itemspropuestas=itemspropuestas,
        isstatic=isstatic)


@blueprint.route("/a/<agenda>", methods=['GET'])
def causa(agenda):
    isstatic = not current_app.config['USE_DIRECTUS']


@blueprint.route("/genero", methods=['GET'])
def genero():
    isstatic = not current_app.config['USE_DIRECTUS']
    if isstatic:
        import app.directus_fake as directus_fake
        dtextos = directus_fake.get_genero_textos()
        dimgs = directus_fake.get_index_imgs()
        dimgsgenero = directus_fake.get_genero_imgs()
        itemsseguidores = directus_fake.get_seguidor_items()
        itemsnovedades = directus_fake.get_novedades_items()
        itemsagenda = directus_fake.get_agenda_items()
        itemstemas = directus_fake.get_temas_items()
    else:
        import app.directus as directus
        dtextos = directus.dapi.get_textos_pagina('Genero')
        dimgs = directus.dapi.get_imgs_pagina('Home')
        dimgsgenero = directus.dapi.get_imgs_pagina('Genero')
        itemsseguidores = directus.dapi.get_items_seguidor()
        itemstemas = directus.dapi.get_items_tema()
        itemsnovedades = directus.dapi.get_items_novedades()
        itemsagenda = directus.dapi.get_items_agenda()
    return render_template(
        'causa.html',
        dtextos=dtextos,
        dimgs=dimgs,
        dimgsgenero=dimgsgenero,
        itemsseguidores=itemsseguidores,
        itemsnovedades=itemsnovedades,
        itemsagenda=itemsagenda,
        itemstemas=itemstemas,
        isstatic=isstatic)
