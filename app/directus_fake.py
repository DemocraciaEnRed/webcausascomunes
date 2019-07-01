
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
            'subtitulo': 'Est nobis dolorem magni qui rerum delectus laborum ipsum.'},
        'novedades': {
            'titulo': 'Últimas novedades',
            'subtitulo': 'Nam libero tempore qui rerum delectus laborum ipsum. Totam dolores totam aspernatur sed.',
            'items': get_novedades_items()},
        'candidates': {
            'titulo': 'Contactá a les candidates',
            'subtitulo': 'Activá la causa que quieras y contales por qué es tan importante.',
            'boton': 'Activá',
            'items': get_novedades_items()},
        'eventos': {
            'titulo': 'Enterate de los próximos eventos',
            'agenda': {
                'titulo': 'Agenda',
                'items': get_agenda_items()
            },
            'novedades': {
                'titulo': '¡Hola! Recibí las últimas novedades en tu correo.',
                'email': {
                    'label':'Tu correo electrónico',
                    'placeholder':'Ej: hola@tuemail.com'
                },
                'ubicacion': {
                    'label':'¿En qué ciudad/provincia votás?',
                    'placeholder':'Ingresá la ciudad o provincia.'
                },
                'boton' : 'Enviar'
            } 
        }
    }


def get_index_imgs():
    return {
        'portada': {
            'imagen': 'portada.svg',
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
        ItemNovedad(8, 'nove1.jpg', 'Título de artículo y/o tema de debate para elecciones.', '#Drogas'),
        ItemNovedad(4, 'nove2.jpg', 'Título de artículo y/o tema de debate para elecciones.', '#Trabajo'),
        ItemNovedad(8, 'nove2.jpg', 'Título de artículo y/o tema de debate para elecciones.', '#Vivienda'),
    ]

class ItemAgenda:
    def __init__(self, fecha, hora, titulo, hashtag):
        self.fecha = fecha
        self.hora = hora
        self.titulo = titulo
        self.hashtag = hashtag

def get_agenda_items():
    return [
        ItemAgenda('Martes 19 de junio', '17:30 hs', 'Título de la actividad que se realizará.', '#Drogas'),
        ItemAgenda('Viernes 5 de julio', '9:00 hs', 'Título de la actividad que se realizará.', '#Trabajo'),
        ItemAgenda('Viernes 5 de julio', '9:00 hs', 'Título de la actividad que se realizará.', '#Trabajo'),
        ItemAgenda('Viernes 5 de julio', '9:00 hs', 'Título de la actividad que se realizará.', '#Trabajo'),
    ]
