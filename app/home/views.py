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
    else:
        import app.directus as directus
        dtextos = directus.dapi.get_textos('Home')
        dimgs = directus.dapi.get_imgs('Home')
        itemsnovedades = directus.dapi.get_itemsnovedades()
        itemsagenda = directus.dapi.get_itemsagenda()
        itemspropuestas = directus.dapi.get_itemspropuestas()
    return render_template(
        'index.html',
        dtextos=dtextos,
        dimgs=dimgs,
        itemsnovedades=itemsnovedades,
        itemsagenda=itemsagenda,
        itemspropuestas=itemspropuestas,
        isstatic=isstatic)

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
        dtextos = directus.dapi.get_textos('Genero')
        dimgs = directus.dapi.get_imgs('Home')
        dimgsgenero = directus.dapi.get_imgs('Genero')
        itemsseguidores = directus.dapi.get_itemsseguidores()
        itemsnovedades = directus.dapi.get_itemsnovedades()
        itemsagenda = directus.dapi.get_itemsagenda()
        itemstemas = directus.dapi.get_itemstemas()
    return render_template(
        'genero.html',
        dtextos=dtextos,
        dimgs=dimgs,
        dimgsgenero=dimgsgenero,
        itemsseguidores=itemsseguidores,
        itemsnovedades=itemsnovedades,
        itemsagenda=itemsagenda,
        itemstemas=itemstemas,
        isstatic=isstatic)
