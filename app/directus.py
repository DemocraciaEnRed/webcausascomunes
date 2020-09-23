# https://github.com/directus/directus-docker
# https://github.com/directus/api-docs-6-legacy
# https://github.com/directus/api-docs-6-legacy/blob/1.1/overview/authentication.md
# https://2.python-requests.org/en/master/
# https://github.com/directus/api-docs-6-legacy/blob/1.1/overview/endpoints.md
import re
import datetime
import requests
from markdown2 import Markdown
from logging import Logger
from .logger import log_err

# api endpoints - https://github.com/directus/api-docs-6-legacy/blob/1.1/overview/endpoints.md
# filterig - https://docs.directus.io/api/reference.html#filtering
class DirectusApi:
    class NoImgException(Exception):
        pass

    class RowTypes:
        TEXT = 0
        IMG = 1
        DATETIME = 2
        REL_NOMBRE = 3
        BOOL = 4
        TOGGLE = 4

    def __init__(self):
        self.logger = None
        self.ser_url = None
        self.ser_ext_url = None
        self.api_url = None
        self.token = None
        self.auth_header = None
        self.textosregx = re.compile('^[^<>]*$')
        self.markdowner = Markdown()
        self._items_novedades_schema = {
            'pagina': DirectusApi.RowTypes.REL_NOMBRE,
            'imagen': DirectusApi.RowTypes.IMG,
            'titulo': DirectusApi.RowTypes.TEXT,
            'texto': DirectusApi.RowTypes.TEXT,
            'url': DirectusApi.RowTypes.TEXT,
            'es_nueva': DirectusApi.RowTypes.TOGGLE,
            'es_destacada': DirectusApi.RowTypes.TOGGLE
        }

    def init_api(self, logger, ser_url, ser_ext_url, api_path, token):
        # chequear parámetros
        assert type(logger) == Logger, 'Se ha proporcionado un logger inválido para Directus'
        assert ser_url, 'No se ha proporcionado una url interna de Directus'
        assert ser_ext_url, 'No se ha proporcionado una url externa de Directus'
        assert api_path, 'No se ha proporcionado un path para la API de Directus'
        assert token, 'No se ha proporcionado un token para Directus'
        assert ser_url.startswith('http'), 'La url interna de Directus debe comenzar con "http" o "https"'
        assert ser_ext_url.startswith('http'), 'La url externa de Directus debe comenzar con "http" o "https"'

        # sanear terminaciones de url
        if ser_url[-1] == '/':
            ser_url = ser_url[:-1]
        if ser_ext_url[-1] == '/':
            ser_ext_url = ser_ext_url[:-1]
        if not api_path[0] == '/':
            api_path = '/' + api_path

        # almacenamos
        self.logger = logger
        self.ser_url = ser_url
        self.ser_ext_url = ser_ext_url
        self.api_url = ser_url + api_path
        self.token = token
        self.auth_header = {'Authorization': 'Bearer ' + self.token}

    def parse_pagina_name(self, pagina):
        pagina_parsed = pagina if pagina.find('-') == -1 else pagina.replace('-', ' ')
        pagina_parsed = pagina_parsed.capitalize()
        return pagina_parsed

    def get(self, api_cmd, **kwargs):
        if 'headers' in kwargs:
            kwargs['headers'].update(self.auth_header)
        else:
            kwargs['headers'] = self.auth_header
        r = requests.get(self.api_url + api_cmd, **kwargs)
        if r.status_code >= 400:
            raise Exception('{} Página no encontrada "{}"'.format(r.status_code, self.api_url + api_cmd))
        if r.text == 'You must be logged in to access the API':
            raise Exception('Mala autenticación al servidor directus')
        try:
            rj = r.json()
        except ValueError:
            raise Exception('El servidor directus devolvió un json inválido al comando ' + api_cmd)
        return rj

    def test_conn(self):
        r = requests.get(self.ser_url + '/server/ping')
        if r.status_code != 200:
            raise Exception('El servidor directus devolvió un error al hacerle ping')
        if 'login.php' in r.url:
            raise Exception('El servidor directus pide login para esa página')
        if r.text != 'pong':
            raise Exception('El servidor directus no responde bien al ping')
        rj = self.get('tables')
        if not rj['data']:
            raise Exception('Mala autenticación al servidor directus')

    def get_table_schema(self, table_name, **kwargs):
        return self.get('tables/' + table_name, **kwargs)

    def get_table_rows(self, table_name, filter=None, **kwargs):
        try:
            rj = self.get('tables/' + table_name + '/rows' + ('?'+filter if filter else ''), **kwargs)
            return rj['data']
        except Exception as e:
            self.logger.error('No se pudieros traer las rows de la tabla "{}" (usando filtro "{}"). {}'.format(table_name, filter, e))
            return []

    def img_row_to_url(self, imgrow, errmsg):
        if imgrow and 'data' in imgrow and 'url' in imgrow['data']:
            return self.ser_ext_url + imgrow['data']['url']
        else:
            self.logger.error('{}'.format(errmsg))
            return ''

    def _parse_ubicacion(self, row_ubicacion):
        ubicacion_arr = []

        ubics = row_ubicacion.split('-')
        for ubic in ubics:
            ubic_parsed = ubic.strip().lower()
            if ubic_parsed.isalnum():
                ubicacion_arr.append(ubic_parsed)
            else:
                return

        return ubicacion_arr

    def get_textos_pagina(self, pagina):
        pagina = str(pagina)
        pagina_parsed = self.parse_pagina_name(pagina)
        if str.isnumeric(pagina):
            filter_by = 'id'
        else:
            filter_by = 'nombre'
        rows = self.get_table_rows('textos', 'filters[pagina.{}][eq]={}'.format(filter_by, pagina_parsed))
        # if not rows:
        #     raise Exception('No se han encontrado textos para la página ' + pagina)
        textos = {}
        for row in rows:
            ubicacion_arr = self._parse_ubicacion(row['ubicacion'])
            if not ubicacion_arr:
                self.logger.error(f'El dato ubicacion="{row["ubicacion"]}" (página={pagina}) en la tabla "textos" tiene caracteres inválidos')
                continue
            else:
                txt = row['texto'] or ''
                if self.textosregx.match(txt) is None:
                    self.logger.error('El dato texto="{}" (página={}) en la tabla "textos" tiene caracteres inválidos'.format(txt, pagina))
                    continue
                if row['con_formato'] == 1:
                    txt = self.markdowner.convert(txt)
                if len(ubicacion_arr) == 1:
                    textos[ubicacion_arr[0]] = txt
                else:
                    if ubicacion_arr[0] not in textos:
                        textos[ubicacion_arr[0]] = {}
                    textos[ubicacion_arr[0]][ubicacion_arr[1]] = txt
        return textos

    def get_imgs_pagina(self, pagina):
        pagina = str(pagina)
        pagina_parsed = self.parse_pagina_name(pagina)
        if str.isnumeric(pagina):
            filter_by = 'id'
        else:
            filter_by = 'nombre'
        rows = self.get_table_rows('imagenes', 'filters[pagina.{}][eq]={}'.format(filter_by, pagina_parsed))
        # if not rows:
        #     raise Exception('No se han encontrado imágenes para la página ' + pagina)
        imgs = {}
        for row in rows:
            ubic_arr = self._parse_ubicacion(row['ubicacion'])
            if ubic_arr:
                imgurl = self.img_row_to_url(row['imagen'], 'Hay una imagen vacía para la ubicacion "{}"'.format(row['ubicacion']))
                if len(ubic_arr) == 1:
                    imgs[ubic_arr[0]] = imgurl
                else:
                    if ubic_arr[0] not in imgs:
                        imgs[ubic_arr[0]] = {}
                    imgs[ubic_arr[0]][ubic_arr[1]] = imgurl
        return imgs

    def get_items(self, table, keys_types, pagina=None, causa=None, filter=None):
        if pagina:
            rows = self.get_table_rows(table, filter='filters[pagina.nombre][eq]={}'.format(pagina.title()))
        elif causa:
            causa_parsed = self.parse_pagina_name(causa)
            rows = self.get_table_rows(table, filter='filters[causa.nombre][eq]={}'.format(causa_parsed))
        elif filter:
            rows = self.get_table_rows(table, filter=filter)
        else:
            rows = self.get_table_rows(table)
        items = []
        for row in rows:
            item = {}
            for key, type in keys_types.items():
                if type == DirectusApi.RowTypes.TEXT:
                    item[key] = row[key] or ''
                elif type == DirectusApi.RowTypes.IMG:
                    item[key] = self.img_row_to_url(row[key], 'Un item de {} no tiene imagen asignada'.format(table)) if row[key] else ''
                elif type == DirectusApi.RowTypes.DATETIME:
                    item[key] = datetime.datetime.strptime(row[key], "%Y-%m-%d %H:%M:%S") if row[key] else datetime.datetime(1,1,1)
                elif type == DirectusApi.RowTypes.REL_NOMBRE:
                    item[key] = row[key]['data']['nombre'].replace(' ', '-') if row[key] and row[key]['data'] else ''
                elif type == DirectusApi.RowTypes.BOOL:
                    item[key] = True if row[key] and row[key] != '0' else False
                else:
                    self.logger.error('Tipo de dato inválido para columna {} (tabla={}, pagina={})'.format(key, table, pagina))
                    continue
            items.append(item)
        return items

    def get_item(self, table, keys_types, pagina=None, causa=None, filter=None):
        items = self.get_items(table, keys_types, pagina, causa, filter)
        return items[0] if items and len(items) else None

    def get_items_novedades(self, pagina):
        return self.get_items(
            'items_novedades',
            self._items_novedades_schema,
            pagina=pagina)

    def get_items_novedades_index(self):
        novedades_nuevas = self.get_items(
            'items_novedades',
            self._items_novedades_schema,
            filter='filters[es_nueva][eq]=1')

        novedades_destacadas = self.get_items(
            'items_novedades',
            self._items_novedades_schema,
            filter='filters[es_destacada][eq]=1')

        return (novedades_nuevas, novedades_destacadas)

    def get_items_propuestas(self):
        return self.get_items('items_propuestas', {
                'titulo': DirectusApi.RowTypes.TEXT,
                'texto': DirectusApi.RowTypes.TEXT,
                'pagina': DirectusApi.RowTypes.REL_NOMBRE
            })

    def get_items_hackaton(self):
        return self.get_items('galeria_hackaton', {
                'titulo': DirectusApi.RowTypes.TEXT,
                'descripcion': DirectusApi.RowTypes.TEXT,
                'imagen_archivo': DirectusApi.RowTypes.TEXT
            })

    def get_items_scrolly(self, causa):
        return self.get_items('scrollytelling', {
                'imagen': DirectusApi.RowTypes.IMG,
                'titulo': DirectusApi.RowTypes.TEXT,
                'texto': DirectusApi.RowTypes.TEXT,
                'css_class': DirectusApi.RowTypes.TEXT
            }, causa=causa)

    def get_item_mapa(self, causa):
        return self.get_item('mapas_causas', {
                'hashtag': DirectusApi.RowTypes.TEXT,
                'titulo': DirectusApi.RowTypes.TEXT,
                'subtitulo': DirectusApi.RowTypes.TEXT,
                'codigo_mapa': DirectusApi.RowTypes.TEXT
            }, causa=causa)

    '''
    def get_items_compromisos(self, causa):
        return self.get_items('imagenes_compromisos', {
                'imagen': DirectusApi.RowTypes.TEXT,
                'descripcion': DirectusApi.RowTypes.TEXT
            }, causa=causa)

    def get_items_agenda(self, pagina):
        return self.get_items('items_agenda', {
                'fechahora': DirectusApi.RowTypes.DATETIME,
                'titulo': DirectusApi.RowTypes.TEXT,
                'hashtag': DirectusApi.RowTypes.TEXT,
                'icono': DirectusApi.RowTypes.IMG
            }, pagina=pagina)

    def get_items_seguidor(self, pagina):
        return self.get_items('items_seguidor', {
                'titulo': DirectusApi.RowTypes.TEXT,
                'imagen': DirectusApi.RowTypes.IMG,
                'url': DirectusApi.RowTypes.TEXT
            }, pagina=pagina)

    def get_items_tema(self, pagina):
        return self.get_items('items_tema', {
                'titulo': DirectusApi.RowTypes.TEXT,
                'texto': DirectusApi.RowTypes.TEXT,
                'imagen': DirectusApi.RowTypes.IMG
            }, pagina=pagina)'''

dapi = DirectusApi()


def init_flask_app(app):
    global dapi
    dapi.init_api(
        app.logger,
        app.config['DIRECTUS_URL_INTERNAL'],
        app.config['DIRECTUS_URL_EXTERNAL'],
        app.config['DIRECTUS_API_PATH'],
        app.config['DIRECTUS_TOKEN'])
    dapi.test_conn()
    return dapi

'''
def auth():
    params = {
        "email": "admin@admin.com",
        "password": "admin"
    }

    r = requests.post('http://localhost:8080/api/1.1/auth/request-token', data=params)
    # r = requests.post('http://localhost:8080/directus/auth/authenticate', auth=("admin@admin.com",'admin'))

    # r = requests.get('http://localhost:8080/server/ping', data=params)
    json = ''
    try:
        json = r.json()
    except ValueError:
        pass
    if json:
        if not json['success']:
            json['error']['message']
        else:
            token = json['data']['token']
            headers = {'Authorization': 'Bearer ' + token}
            r = requests.get('http://localhost:8080/api/1.1/tables', headers=headers)
            json = r.text
            r = requests.get('http://localhost:8080/api/1.1/tables/textos/rows', headers=headers)
            json += ';;;;' + r.text
            # ret 401 on bad token
    return str(r.status_code) + '-' + r.text + '@' + str(json)
'''
