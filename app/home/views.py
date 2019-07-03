from flask import current_app, render_template, Blueprint
import locale

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
        locale.setlocale(locale.LC_TIME, 'es_AR.UTF-8')
    return render_template(
        'index.html',
        dtextos=dtextos,
        dimgs=dimgs,
        itemsnovedades=itemsnovedades,
        itemsagenda=itemsagenda,
        itemspropuestas=itemspropuestas,
        isstatic=isstatic)
