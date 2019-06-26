
def get_index_textos():
    return {
        'portada': {
            'titulo': 'Causas comunes',
            'subtitulo': 'Todo aquello que querías saber sobre',
            'boton': 'Ver más'},
        'manifiesto': {
            'titulo': 'Nuestro manifiesto',
            'parrafo1': 'Est nobis dolorem magni qui rerum delectus laborum ipsum. Totam dolores totam aspernatur sed. Temporibus autem voluptatem sunt aliquam sit debitis et illo. Velit nostrum sit animi necessitatibus sed impedit delectus. Aperiam amet perferendis officiis ad amet ab voluptas. Suscipit ipsa reiciendis eveniet. Necessitatibus ipsum ut est repellendus exercitationem. Voluptate non aperiam accusamus omnis quia eaque eum nostrum. Modi quibusdam quam et. Corrupti officiis sunt sit et maxime sed ipsa modi. Ipsum eveniet omnis eum magni. Magni temporibus cupiditate eum culpa maxime. Harum esse rem ad nihil rerum. Provident aut qui mollitia neque earum minima ducimus. Nemo vel maxime unde et at. Quo cum doloremque ut ad in. Atque quia eveniet quas est non. Esse magnam qui qui inventore consequatur non itaque delectus. Veritatis laborum beatae est. Sed nostrum qui aperiam. Est laudantium dignissimos iste labore voluptatem ea. Corporis rerum quidem molestiae dolor.',
            'parrafo2': 'Est nobis dolorem magni qui rerum delectus laborum ipsum. Totam dolores totam aspernatur sed. Temporibus autem voluptatem sunt aliquam sit debitis et illo. Velit nostrum sit animi necessitatibus sed impedit delectus. Aperiam amet perferendis officiis ad amet ab voluptas. Suscipit ipsa reiciendis eveniet. Necessitatibus ipsum ut est repellendus exercitationem. Voluptate non aperiam accusamus omnis quia eaque eum nostrum. Modi quibusdam quam et. Corrupti officiis sunt sit et maxime sed ipsa modi. Ipsum eveniet omnis eum magni. Magni temporibus cupiditate eum culpa maxime. Harum esse rem ad nihil rerum. Provident aut qui mollitia neque earum minima ducimus. Nemo vel maxime unde et at. Quo cum doloremque ut ad in. Atque quia eveniet quas est non. Esse magnam qui qui inventore consequatur non itaque delectus. Veritatis laborum beatae est. Sed nostrum qui aperiam. Est laudantium dignissimos iste labore voluptatem ea. Corporis rerum quidem molestiae dolor.'},
        'propuestas': {
            'titulo': 'Conocé las propuestas',
            'subtitulo': 'Est nobis dolorem magni qui rerum delectus laborum ipsum. Totam dolores totam aspernatur sed. Temporibus autem voluptatem sunt aliquam sit debitis et illo. Velit nostrum sit animi necessitatibus sed impedit delectus.'},
        'novedades': {
            'titulo': 'Últimas novedades',
            'subtitulo': 'Nam libero tempore qui rerum delectus laborum ipsum. Totam dolores totam aspernatur sed. Temporibus autem voluptatem sunt aliquam sit debitis et illo. Velit nostrum sit animi necessitatibus sed impedit delectus.',
            'items': get_novedades_items()},
        'candidates': {
            'titulo': 'Contactá a les candidates',
            'subtitulo': 'Activá la causa que quieras y contales por qué es tan importante.',
            'boton': 'Activá',
            'items': get_novedades_items()}
    }


def get_index_imgs():
    return {
        'portada': {
            'fondo': 'portada.jpg',
        },
        'candidates': {
            'imagen': 'nove2.jpg'
        }
    }


class ItemNovedad:
    def __init__(self, ancho_columnas, imgurl, titulo, texto):
        self.ancho_columnas = ancho_columnas
        self.imgurl = imgurl
        self.titulo = titulo
        self.texto = texto


def get_novedades_items():
    return [
        ItemNovedad(4, 'nove1.jpg', 'Un titulo1', 'sad kasd kjsa jas djklasdjas  askljc asc klascjk acicuq iweuqw skj'),
        ItemNovedad(8, 'nove2.jpg', 'Un titulo2', 'ty  jnbvn fgghd ud gfdfhfgdb   fgdjas  askljc asc klascjw askj'),
        ItemNovedad(6, 'nove2.jpg', 'Un titulo56', 'uiopupiolasdjas  askljc asc klascjk acicuq iweuqw askj'),
        ItemNovedad(3, 'nove1.jpg', 'Un titulo23', 'sb v a jas djklasdjas  askljc asc klascjk acicuq iweuqw askj'),
        ItemNovedad(3, 'nove1.jpg', 'Un titulo34', 'sa24 22632352 5klasdjas  askljc asc klascjk acicuq iweuqw askj')
    ]
