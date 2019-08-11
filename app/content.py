'''
dtextos = directus.dapi.get_textos_pagina('Home')
dimgs = directus.dapi.get_imgs_pagina('Home')
itemspropuestas = directus.dapi.get_items_propuestas()
# itemsnovedades = directus.dapi.get_items_novedades('Home')
itemsagenda = directus.dapi.get_items_agenda('Home')
galeriahackaton = directus.dapi.get_items_hackaton()
'''

def slash_dict_to_dual_dict(slash_dict):
    dual_dict = {}
    for (k,v) in slash_dict.items():
        k_sp = k.split('-')
        if len(k_sp) == 1:
            dual_dict[k] = v
        else:
            k1 = k_sp[0]
            k2 = k_sp[1]
            if k1 in dual_dict:
                dual_dict[k1].update({k2: v})
            else:
                dual_dict[k1] = {k2: v}
    return dual_dict


def textos_home():
    txts = {
        'wiki-titulo': 'Wiki de Causas Comunes',
        'wiki-subtitulo': '''El conocimiento es una construcción social, por eso vamos a usar Wikis para exponer a fondo nuestras causas comunes.

Te proponemos sumarte a compartir datos, fuentes y escribir sobre cada causa. Queremos generar entradas enciclopédicas que sirvan como diagnósticos y referencias para mejores políticas públicas.
''',
        'wiki-boton': 'Sumate!',

        'propuestas-titulo': 'Conocé nuestras causas',
        'propuestas-subtitulo': '',

        'hackaton-titulo': 'Hackaton de Causas Comunes en la Facultad de Derecho',
        'hackaton-subtitulo': 'Causas Comunes pretende ser un espacio para hacer converger demandas que venimos impulsando desde organizaciones, redes, activistas, intelectuales, y que queremos que estén en las agendas de les candidates que se postulan en estas elecciones legislativas. Para consolidar y darle fuerza a este espacio de reunión, el sábado 13 de julio organizamos una hackaton en la Facultad de Derecho de la UBA. Reunides en grupos en torno a cada causa común, comenzamos a delimitar los ejes y aportar entre todes datos concretos que respalden nuestras propuestas. Queremos que les candidates asuman compromisos y por eso nos reunimos a elaborar cómo vamos a presentar nuestras demandas.',

        'agenda-titulo': '',
        'agenda-subtitulo': '¡Seguinos!',

        'correo-titulo': '',
        'correo-email': '',
        'correo-emailsub': '',
        'correo-ubicacion': '',
        'correo-ubicacionsub': '',
        'correo-boton': '',

        'video': 'https://www.youtube.com/embed/NOhxxzuihnU',
        'manifiesto-titulo': '',
        'manifiesto-parrafo1': 'Somos ecologistas, feministas, personas preocupadas por la precarización laboral y la ausencia de políticas públicas que nos garanticen trabajo y vivienda digna. Venimos construyendo alternativas, movilizándonos, encontrándonos en las calles, en las redes, desde diversos espacios y territorios. Tenemos ideas, tenemos propuestas y buscamos que tengan impacto real. Queremos copar el espacio electoral y aportar a una democracia con mayor participación de todes; que las elecciones no queden en ir a votar y nada más. Queremos estimular el debate y aportar con soluciones concretas porque no estamos dispuestos/as a seguir postergando cuestiones que necesitan ser resueltas hoy. Desde Causas Comunes vamos a incidir para que en estas Elecciones 2019 escuchemos compromisos de nuestros/as candidatos/as con respecto a las políticas sobre drogas, la transparencia, nuestros derechos laborales, con perspectivas amplias, inclusivas y diversas. !Sumate!',
        'manifiesto-firma': ' Causas Comunes ',

        'portada-titulo': '',
        'portada-subtitulo': '',
        'portada-boton': 'Ver más'
    }
    return slash_dict_to_dual_dict(txts)


'''
for itm in itemspropuestas %}
{{create_item_propuesta(itm.get('imagen_fondo'), itm.get('icono'), itm.get('titulo'), itm.get('texto'),
                        itm.get('pagina'))}}
'''
def items_propuestas():
    data_arrs=[
        ['Trabajo', 'Trabajo', 'Los derechos laborales y las nuevas tecnologías, un conflicto abierto en un país precarizado.'],
        ['Ambiente', 'Ambiente', 'El cuidado del ambiente no es un lujo ni se puede postergar, es una necesidad urgente. '],
        ['genero', 'Género', 'Las elecciones 2019 estrenan paridad en las listas, ¿avanza la agenda feminista? '],
        ['Vivienda', 'Vivienda', 'La defensa de nuestros derechos en el reino de la especulación y la incertidumbre. '],
        ['Drogas', 'Drogas', 'Por una regulación de la producción, comercialización, y tenencia para consumo.'],
        ['Transparencia', 'Transparencia', 'La transparencia es condición para la democracia, pero ¿más transparencia es más justicia?'],
        ['Ciencia', 'Ciencia', ' Sin ciencia no hay futuro']
    ]
    ret_dict_arr = []
    for arr in data_arrs:
        ret_dict_arr.append({
            'imagen_fondo': '',
            'icono': '',
            'titulo': arr[1],
            'texto': arr[2],
            'pagina': arr[0].lower(),
        })
    return ret_dict_arr


'''
{% for itm in galeriahackaton %}
    {{ create_item_galeria(itm.get('titulo'), itm.get('descripcion'), itm.get('imagen_archivo')) }}
{% endfor %}'''
def items_hackaton():
    tit = 'Hackaton en Derecho (UBA)'
    imgs=[
        'IMG_8857.JPG',
        'IMG_8865.JPG',
        'IMG_8882.JPG',
        'IMG_8901.JPG',
        'IMG_8939.JPG',
        'IMG_20190713_132939.jpg',
        'IMG_3477.JPG',
        'IMG_3488.JPG',
        'IMG_3508.JPG',
    ]
    ret_dict_arr = []
    for img in imgs:
        ret_dict_arr.append({
            'titulo': tit,
            'descripcion': tit,
            'imagen_archivo': img
        })
    return ret_dict_arr