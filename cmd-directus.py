import os, sys
import requests
from pprint import pprint

def ret_err(msg):
    print('Error:', msg)
    sys.exit(1)

cmd = sys.argv[1] if len(sys.argv) > 1 else None
if not cmd:
    ret_err('El script se usa proporcionando mínimamente 1 argumento')

token = os.environ.get('DIRECTUS_TOKEN')
if not token:
    ret_err('Debe proporcionar DIRECTUS_TOKEN')


auth_header = {'Authorization': 'Bearer ' + token}
api_url = 'https://directus.democraciaenred.org/api/1.1/'


def api_get(query):
    return requests.get(api_url + query, headers=auth_header).json()['data']
def api_put(query, data):
    return requests.put(api_url + query, headers=auth_header, data=data)
def api_post(query, data):
    return requests.post(api_url + query, headers=auth_header, data=data)


def api_txt_lock(lock_num):
    data_pagina = {'options': '{"id":"many_to_one","read_only":'+str(lock_num)+',"visible_column":"nombre","visible_column_template":"{{nombre}}"}'}
    print('pagina', api_put('tables/textos/columns/pagina', data_pagina))
    data = {'options': f'{{"id":"toggle","read_only":{lock_num}}}'}
    print('ubicacion', api_put('tables/textos/columns/ubicacion', data))
    # cambia el read_only pero directus no da bola y podés cambiar el valor igual
    # print('con_formato', api_put('tables/textos/columns/con_formato', data))
def api_txt_add(pagina, ubicacion, texto, con_formato):
    data = {
        'pagina': pagina,
        'ubicacion': ubicacion,
        'texto': texto,
        'con_formato': con_formato
    }
    return api_post('tables/textos/rows', data)
def api_img_add(pagina, ubicacion):
    data = {
        'pagina': pagina,
        'ubicacion': ubicacion
    }
    return api_post('tables/imagenes/rows', data)


pags = {}
def load_pags():
    pag_rows = api_get('tables/paginas/rows')
    for p in pag_rows:
        pags[p['nombre'].lower()] = p['id']

causas_nombres = ['Transparencia', 'Ambiente', 'Vivienda', 'Trabajo',
                  'Ciencia', 'Drogas', 'Genero']

# print( api_get('tables/imagenes_compromisos/rows') )
# sys.exit(0)
# api endpoints - https://github.com/directus/api-docs-6-legacy/blob/1.1/overview/endpoints.md
# pprint(api_get(''))
if cmd == 'txtlocked':
    r = api_get('tables/textos/columns/con_formato')
    print(r['options']['read_only'] == 1)

elif cmd == 'txtlock':
    api_txt_lock(1)

elif cmd == 'txtunlock':
    api_txt_lock(0)

elif cmd == 'getpags':
    pprint(api_get('tables/paginas/rows'))

elif cmd == 'txtadd':
    if not len(sys.argv) >= 4: ret_err('Para agregar un texto debe proporcionar al menos 2 argumentos después del comando')
    if not pags: load_pags()
    for a in sys.argv:
        if a == '-':
            ret_err('El argumento de ubicación debe estar entre comillas si tiene guión "-", o con las palabras pegadas')

    pag_arg = sys.argv[2]
    if pag_arg.isnumeric():
        pag_id = int(pag_arg)
    elif pag_arg in pags:
        pag_id = pags[pag_arg]
    else:
        pag_id = None
        for p in pags.keys():
            if p.startswith(pag_arg):
                pag_id = pags[p]
                break
        if not pag_id:
            ret_err(f'Página "{pag_arg}" inválida')
    ubi_arg = sys.argv[3].title()
    if '-' in ubi_arg and ' - ' not in ubi_arg:
        ubi_arg = ubi_arg.replace('-', ' - ')
    txt_arg = sys.argv[4] if len(sys.argv) >= 5 else ''
    fmt_arg = sys.argv[5] if len(sys.argv) >= 6 else '0'
    if not fmt_arg.isnumeric():
        ret_err('El argumento de formato debe ser 0 o 1')

elif cmd == 'txtsadd':
    if not pags: load_pags()
    causas_ids_no_trabaj = [12, 7, 8, 10, 11, 4]
    for c in causas_ids_no_trabaj:
        print(api_img_add(c, 'Compromisos - Imagen'))

elif cmd == 'imgadd':
    #ret_err('No implementada')
    #sys.exit(1)
    #if not pags: load_pags()
    #causas_ids = [12, 7, 8, 9, 10, 11, 4]
    #causas_ids_no_trabaj = [12, 7, 8, 10, 11, 4]
    #for c in causas_ids_no_trabaj:
    #    print(c, api_txt_add(c, 'Compromisos - Texto', link, 1))
    print(api_txt_add(12, 'Compromisos - Texto', '''En la última semana hubo intercambios en torno al sistema mediante el cual se realizará el escrutinio en las PASO. Es que el gobierno mostró a los partidos un tutorial sobre cómo funciona el software de SmartMatic, pero no entregó el código fuente, ya que pertenece a una empresa privada. A partir de esto, se generó un conflicto en torno a dejar el acto electoral en manos de empresas y acerca de la transparencia del proceso.
El candidato a presidente Alberto Fernández (Frente de Todos) presentó un amparo para apartar a SmartMatic de la elección y volver al método anterior. Sostienen que si el gobierno no entregó a revisión este software hace un mes cuando debía hacerlo, es porque sabe que es vulnerable. Por su parte, el Ministro del Interior Rogelio Frigerio (Cambiemos) rápidamente desmintió que haya posibilidad de fraude con este sistema. Más allá del fraude, se advierte que puede haber errores en el conteo provisorio. 
Podés leer el informe completo de la Fundación Vía Libre en donde se detallan las vulnerabilidades del sistema y se solicita a las autoridades electorales que se comprometan a resguardar la seguridad del escrutinio.''', 1))
    print(api_txt_add(4, 'Compromisos - Texto', '''Hoy se cumple un año del rechazo al proyecto de Ley de Interrupción Voluntaria del Embarazo en el Senado. Podés ver cómo votaron les senadores el año pasado en la página de Activá el Congreso. También podés dejarles mensajes por esa vía. 
Cuando repasamos el posicionamiento de lxs candidatxs a presidente encontramos que solo tres de ellxs están a favor del aborto legal, seguro y gratuito: Alberto Fernández, Nicolás del Caño (FIT - Unidad) y Manuela Castañeira (Nuevo MAS). Los demás candidatos están en contra. Biondini (Frente Patriota) y Gómez Centurión (Frente Nos) incluso centraron su spots de campaña en su posición “pro-vida”. El único dudoso es José Luis Espert (Despertar), que en varias entrevistas se manifestó a favor, pero a la vez se opone a que sea gratuito, uno de los ejes de la Campaña. Además señala que le parece un tema “menor”.
Si querés más información, en FeminIndex encontrás la posición y compromisos actuales con los derechos sexuales y reproductivos de unes 80 candidates. ''', 1))
    print(api_txt_add(7, 'Compromisos - Texto', '''El sábado pasado, activistas de Greenpeace aprovecharon un acto oficial en La Rural, al que asistieron Macri y Vidal, entre otres, para llamar la atención sobre la desforestación. Desplegaron carteles justo enfrente del Presidente que decían Basta de Desmontes. Desde la ONG aseguraron que la ganadería intensiva está destruyendo los bosques a gran velocidad y que esto redunda en situaciones como la del yaguareté, que está en extinción y solo quedan 20 especímenes en el Gran Chaco.
La agenda ambiental empezó a cobrar visibilidad gracias a manifestaciones cada vez más recurrentes. En esta nota de La Nación lxs candidatxs responden cuál es el lugar que ocupa este tema en sus plataformas. 
En general, todes hablan de la importancia del tema para el futuro con excepción de José Luis Espert, quien dice que no son muy "obsesivos con eso" y que se puede conjugar fácilmente desarrollo y medio ambiente. Alberto Fernández expresa su preocupación "porque es nuestra casa". Roberto Lavagna (Consenso Federal) plantea que para la juventud es una cuestión de gran importancia así como para su partido. Sin embargo, les únicxs candidatxs que hablan del desmonte, el fracking, la megaminería y el uso de agrotóxicos son Nicolás Del Caño (ver SPOT) y Manuela Castañeira. Vaca Muerta es parte del programa económico de todos los partidos, sin embargo sigue abierta la incógnita de cómo se puede pensar en este camino en el marco de una Crisis Climática.''', 1))
    print(api_txt_add(11, 'Compromisos - Texto', '''La marihuana entró también al debate de campaña. Nicolás del Caño, Manuela Castañeira, José Luis Espert y Alberto Fernández  se muestran a favor de la despenalización. Roberto Lavagna mantiene una posición abierta: "Yo creo que es un debate que vale la pena. Me gustaría que cuando tengamos que decidir, por lo menos tengamos un poco más de información".
María Eugenia Vidal, candidata a gobernadora de la Provincia de Buenos Aires por Juntos por el Cambio, dijo en una entrevista reciente: "Entiendo que puede haber sectores que tengan libertad de decidir, en el caso de la marihuana, fumarse un porro. En algún nivel socioeconómico distinto. Ahora, cuando yo voy a los barrios más pobres de la provincia, el mensaje tiene que ser uno solo porque la marihuana, al igual que el alcohol y el paco, son drogas de inicio". Desde su perspectiva no es momento de dar ese debate. Por su parte, Cristian Ritondo (Juntos por el Cambio) dijo que está de acuerdo en la penalización. ''', 1))
    print(api_txt_add(8, 'Compromisos - Texto', '''En su Newsletter semanal, Fernando Bercovich hace un repaso de las diferentes propuestas de los presidentes con respecto a la temática de vivienda. El Frente de Todos propuso crear un Ministerio de Hábitat y Vivienda “para atender la situación de la gente que está en la calle y de la clase media”. Juntos por el Cambio tiene una propuesta mas general que tiene que ver con la dimensión estructural de la pobreza y mejorar la calidad de vida en las ciudades. Para Roberto Lavagna es prioritario encontrar los mecanismos financieros que posibiliten la implementación efectiva de la ley que establezca el acceso a la propiedad de la tierra y la vivienda digna. El FIT propone medidas que abarcan un plan nacional de viviendas populares de calidad, la urbanización de las villas y asentamientos e impuestos progresivos a las viviendas ociosas.''', 1))
    '''for a in sys.argv:
        if a == '-':
            ret_err('El argumento de ubicación debe estar entre comillas si tiene guión "-", o con las palabras pegadas')

    pag_arg = sys.argv[2]
    if pag_arg.isnumeric():
        pag_id = int(pag_arg)
    elif pag_arg in pags:
        pag_id = pags[pag_arg]
    else:
        pag_id = None
        for p in pags.keys():
            if p.startswith(pag_arg):
                pag_id = pags[p]
                break
        if not pag_id:
            ret_err(f'Página "{pag_arg}" inválida')
    ubi_arg = sys.argv[3].title()
    if '-' in ubi_arg and ' - ' not in ubi_arg:
        ubi_arg = ubi_arg.replace('-', ' - ')

    print(api_img_add(pag_id, ubi_arg))'''

elif cmd == 'txtcausasadd':
    # comentar esta línea y reescribir el código para usar este comando
    ret_err('Este comando fue usado en el pasado, se debe reescribir darle un significado')
    load_pags()
    causas = [
        'genero',
        'ambiente',
        'ciencia',
        'vivienda',
        'transparencia',
        'drogas',
        'trabajo']
    for c in causas:
        if c == 'genero':
            link = 'https://diagnostico.causascomunes.org/index.php/Género'
        else:
            link = 'https://diagnostico.causascomunes.org/index.php/' + c.title()
        print(c, api_txt_add(pags[c], 'Definicion - LinkWiki', link, 0))


else:
    ret_err(f'Comando "{cmd}" inválido. Solo válidos: txtlocked, txtlock, txtunlock, getpags, txtadd, txtcausasadd')
