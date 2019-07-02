import datetime


def get_index_textos():
    return {
        'portada': {
            'titulo': 'Causas comunes',
            'subtitulo': 'Todo aquello que querías saber sobre les candidates y sus propuestas.',
            'boton': 'Ver más'},
        'manifiesto': {
            'titulo': 'Nuestro manifiesto',
            'parrafo1': 'Est nobis dolorem magni qui rerum delectus laborum ipsum. Totam dolores totam aspernatur sed. Temporibus autem voluptatem sunt aliquam sit debitis et illo. Velit nostrum sit animi necessitatibus sed impedit delectus. Aperiam amet perferendis officiis ad amet ab voluptas. Suscipit ipsa reiciendis eveniet. Necessitatibus ipsum ut est repellendus exercitationem. Voluptate non aperiam accusamus omnis quia eaque eum nostrum. Modi quibusdam quam et. Corrupti officiis sunt sit et maxime sed ipsa modi. Ipsum eveniet omnis eum magni.',
            'firma': 'Causas Comunes'},
        'propuestas': {
            'titulo': 'Conocé las propuestas',
            'subtitulo': 'Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus.'},
        'novedades': {
            'titulo': 'Últimas novedades',
            'subtitulo': 'Nam libero tempore qui rerum delectus laborum ipsum. Totam dolores totam aspernatur sed.',
            'items': get_novedades_items()},
        'candidates': {
            'titulo': 'Contactá a les candidates',
            'subtitulo': 'Activá la causa que quieras y contales por qué es tan importante.',
            'boton': 'Activá'},
        'agenda': {
            'titulo': 'Enterate de los próximos eventos',
            'subtitulo': 'Agenda',
            'items': get_agenda_items()
        },
        'correo': {
            'titulo': '¡Hola! Recibí las últimas novedades en tu correo.',
            'email': 'Tu correo electrónico',
            'emailsub': 'Ej: hola@tuemail.com',
            'ubicacion': '¿En qué ciudad/provincia votás?',
            'ubicacionsub': 'Ingresá la ciudad o provincia.',
            'boton': 'Enviar'
        }
    }


def get_index_imgs():
    return {
        'portada': {
            'imagen': 'portada.svg',
            'menu': 'menu.svg',
            'logo': 'logo.svg',
            'search': 'search.svg',
        },
        'manifiesto': {
            'imagen': 'manifiesto.svg',
        },
        'candidates': {
            'imagen': 'candidates.svg'
        }
    }


class ItemNovedad:
    def __init__(self, ancho_columnas, imgurl, titulo, hashtag):
        self.ancho_columnas = ancho_columnas
        self.imgurl = imgurl
        self.titulo = titulo
        self.hashtag = hashtag


def get_novedades_items():
    return [
        ItemNovedad(8, 'novedades1.png', 'Título de artículo y/o tema de debate para elecciones.', 'drogas'),
        ItemNovedad(4, 'novedades2.png', 'Título de artículo y/o tema de debate para elecciones.', 'trabajo'),
        ItemNovedad(8, 'novedades3.png', 'Título de artículo y/o tema de debate para elecciones.', 'vivienda'),
    ]


class ItemAgenda:
    def __init__(self, fechahora, titulo, hashtag):
        self.fechahora = fechahora
        self.titulo = titulo
        self.hashtag = hashtag


def get_agenda_items():
    return [
        ItemAgenda(datetime.datetime(2019, 5, 19, 17, 30), 'Título de la actividad que se realizará.', 'drogas'),
        ItemAgenda(datetime.datetime(2019, 6, 5, 9), 'Título de la actividad que se realizará.', 'trabajo'),
        ItemAgenda(datetime.datetime(2019, 6, 5, 9), 'Título de la actividad que se realizará.', 'vivienda'),
        ItemAgenda(datetime.datetime(2019, 6, 5, 9), 'Título de la actividad que se realizará.', 'genero'),
    ]


class ItemPropuesta:
    def __init__(self, bgimg, icon, title, text):
        self.bgimg = bgimg
        self.icon = icon
        self.title = title
        self.text = text


def get_propuesta_items():
    return [
        ItemPropuesta('propuesta1.png', '', 'Género', 'Cada vez ocupa un lugar más importante en el debate público, sin embargo todavía no está asimilada en las plataformas políticas. '),
        ItemPropuesta('propuesta1.png', '', 'Ambiente', 'Las temáticas ambientales suelen quedar en un segundo plano en las discusiones de desarrollo productivo, se las trata...'),
        ItemPropuesta('propuesta1.png', '', 'Ciencias', 'La situación de los ámbitos científicos en el país es alarmante. Las universidades y escuelas públicas cada vez tienen...'),
        ItemPropuesta('propuesta1.png', '', 'Trabajo', ''),
        ItemPropuesta('propuesta1.png', '', 'Vivienda', '')
    ]
