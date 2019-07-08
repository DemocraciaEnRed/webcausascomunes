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


def get_footer_imgs():
    return {
        'logo': '',
        'social': {
            'facebook': '',
            'twitter': '',
            'instagram': ''
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
        ItemPropuesta('propuesta1.png', 'icono_Género_Outline.png', 'Género', 'Cada vez ocupa un lugar más importante en el debate público, sin embargo todavía no está asimilada en las plataformas políticas. '),
        ItemPropuesta('propuesta1.png', 'icono_Ambiente_Outline.png', 'Ambiente', 'Las temáticas ambientales suelen quedar en un segundo plano en las discusiones de desarrollo productivo, se las trata...'),
        ItemPropuesta('propuesta1.png', 'icono_Ciencia_Outline.png', 'Ciencias', 'La situación de los ámbitos científicos en el país es alarmante. Las universidades y escuelas públicas cada vez tienen...'),
        ItemPropuesta('propuesta1.png', 'icono_Vivienda_Outline.png', 'Trabajo', 'Est nobis dolorem magni qui rerum delectus laborum ipsum. Totam dolores totam aspernatur sed. '),
        ItemPropuesta('propuesta1.png', 'icono_Vivienda_Outline.png', 'Vivienda', 'Est nobis dolorem magni qui rerum delectus laborum ipsum. Totam dolores totam aspernatur sed. ')
    ]


def get_genero_textos():
    return {
        'portada': {
            'titulo': 'Agenda de Género'
        },
        'definicion': {
            'titulo': 'De qué se trata?',
            'parrafo1': 'La agenda de género cada vez ocupa un lugar más importante en el debate público, sin embargo todavía no está asimilada en las plataformas políticas.',
            'parrafo2': 'Las desigualdades se observan tanto en la participación política de las mujeres como en su acceso al mercado laboral donde son mayoría entre las personas desocupadas y precarizadas.',
            'parrafo3': 'A su vez, el trabajo doméstico no remunerado recae asimétricamente sobre ellas generando obstáculos para la inserción laboral y la independencia económica. La violencia machista, la homofobia y transfobia continúan siendo un límite para el ejercicio de derechos.',

        },
        'temas': {
            'titulo': 'Temas',
            'subtitulo': 'Conocé sobre qué se tratará en la Agenda de Género.'
        },
        'seguidores': {
            'titulo': 'Quiénes siguen la Agenda de Género',
            'subtitulo': 'Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus.'
        },
        'actividades': {
            'titulo': 'Qué hacemos',
            'subtitulo': 'Todas las acciones, actividades y agenda sobre Género.'
        },
        'agenda': {
            'titulo': 'Agenda',
            'subtitulo': 'Seguí día a día qué hacemos'
        }
    }


def get_genero_imgs():
    return {
        'definicion': {
            'imagen': 'placeholder.png'
        }
    }


class ItemSeguidor:
    def __init__(self, img, title):
        self.img = img
        self.title = title


def get_seguidor_items():
    return [
        ItemSeguidor('placeholder-circle.png', 'Economía Feminista'),
        ItemSeguidor('placeholder-circle.png', 'Agencia Presentes'),
        ItemSeguidor('placeholder-circle.png', 'FemHackARG')
    ]


class ItemTema:
    def __init__(self, img, title, text):
        self.img = img
        self.title = title
        self.text = text


def get_temas_items():
    return [
        ItemTema('placeholder.png', 'Promoción de la participación política de las mujeres', 'Vivamus luctus nunc a libero molestie, malesuada ornare elit condimentum. Phasellus posuere est metus, non aliquam dolor aliquam in. Praesent vitae enim ipsum. Vivamus non ante odio. Pellentesque consectetur facilisis bibendum. Duis sed porta ligula, quis malesuada turpis. Vivamus lorem nulla, laoreet euismod risus non, dapibus semper dui. Sed at erat ipsum. Morbi eros ipsum, scelerisque eu urna ut, sollicitudin hendrerit tortor. Sed egestas risus magna, a lobortis dui scelerisque vitae. Nunc rhoncus mauris dapibus leo sodales porttitor. Donec magna turpis, tincidunt sed pharetra non, condimentum nec sapien. Sed congue scelerisque semper. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Phasellus blandit auctor mauris non rhoncus. Nam quis nulla enim. Quisque non odio elit. Proin auctor pharetra metus id commodo. Fusce sed justo augue. Proin pellentesque, nulla nec tincidunt sollicitudin, diam tortor congue justo, ac molestie urna magna eu nibh. Aenean nec purus venenatis velit euismod laoreet.'),
        ItemTema('placeholder.png', 'Aborto legal, seguro y gratuito', 'Vivamus luctus nunc a libero molestie, malesuada ornare elit condimentum. Phasellus posuere est metus, non aliquam dolor aliquam in.'),
        ItemTema('placeholder.png', 'Sistema de cuidados', 'Vivamus luctus nunc a libero molestie, malesuada ornare elit condimentum. Phasellus posuere est metus, non aliquam dolor aliquam in.'),
        ItemTema('placeholder.png', 'Cupo Laboral Trans', 'Vivamus luctus nunc a libero molestie, malesuada ornare elit condimentum. Phasellus posuere est metus, non aliquam dolor aliquam in.'),
        ItemTema('placeholder.png', 'Lucha contra la violencia de género', 'Vivamus luctus nunc a libero molestie, malesuada ornare elit condimentum. Phasellus posuere est metus, non aliquam dolor aliquam in.')
    ]
