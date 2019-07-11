# https://github.com/directus/directus-docker
# https://github.com/directus/api-docs-6-legacy
# https://github.com/directus/api-docs-6-legacy/blob/1.1/overview/authentication.md
# https://2.python-requests.org/en/master/
# https://github.com/directus/api-docs-6-legacy/blob/1.1/overview/endpoints.md
import requests
import re
import datetime


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

    def __init__(self):
        self.ser_url = None
        self.ser_ext_url = None
        self.api_url = None
        self.token = None
        self.auth_header = None
        self.textosregx = re.compile('^[^<>&]*$')

    def init_api(self, ser_url, ser_ext_url, api_path, token):
        if ser_url[-1] == '/':
            ser_url = ser_url[:-1]
        if ser_ext_url[-1] == '/':
            ser_ext_url = ser_ext_url[:-1]
        if not api_path[0] == '/':
            api_path = '/' + api_path
        self.ser_url = ser_url
        self.ser_ext_url = ser_ext_url
        self.api_url = ser_url + api_path
        self.token = token
        self.auth_header = {'Authorization': 'Bearer ' + self.token}

    def get(self, api_cmd, **kwargs):
        if 'headers' in kwargs:
            kwargs['headers'].update(self.auth_header)
        else:
            kwargs['headers'] = self.auth_header
        r = requests.get(self.api_url + api_cmd, **kwargs)
        if r.status_code >= 400:
            raise Exception('Mala autenticación al servidor directus'.format(r.status_code, api_cmd))
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
        if r.text != 'pong':
            raise Exception('El servidor directus no responde bien al ping')
        rj = self.get('tables')
        if not rj['data']:
            raise Exception('Mala autenticación al servidor directus')

    def get_table_schema(self, table_name, **kwargs):
        return self.get('tables/' + table_name, **kwargs)

    def get_table_rows(self, table_name, filter=None, **kwargs):
        rj = self.get('tables/' + table_name + '/rows' + ('?'+filter if filter else ''), **kwargs)
        return rj['data']

    def img_row_to_url(self, imgrow, errmsg):
        if not imgrow:
            raise DirectusApi.NoImgException(errmsg)
        return self.ser_ext_url + imgrow['data']['url']

    def get_textos_pagina(self, pagina):
        pagina = str(pagina)
        if str.isnumeric(pagina):
            filter_by = 'id'
        else:
            filter_by = 'nombre'
        rows = self.get_table_rows('textos', 'filters[pagina.{}][eq]={}'.format(filter_by, pagina))
        # if not rows:
        #     raise Exception('No se han encontrado textos para la página ' + pagina)
        textos = {}
        for row in rows:
            ubic = row['ubicacion'].split('-')
            ubicfmt = []
            for ubi in ubic:
                ubicfmt.append(ubi.strip().lower())
                if not ubicfmt[-1].isalnum():
                    raise Exception('El dato de ubicacion "{}" en la tabla de textos tiene caractéres inválidos'.format(ubicfmt[-1]))
            txt = row['texto'] or ''
            if self.textosregx.match(txt) is None:
                raise Exception('El dato de texto "{}" en la tabla de textos tiene caractéres inválidos'.format(txt))
            if len(ubic) == 1:
                textos[ubicfmt[0]] = txt
            else:
                if ubicfmt[0] not in textos:
                    textos[ubicfmt[0]] = {}
                textos[ubicfmt[0]][ubicfmt[1]] = txt
        return textos

    def get_imgs_pagina(self, pagina):
        pagina = str(pagina)
        if str.isnumeric(pagina):
            filter_by = 'id'
        else:
            filter_by = 'nombre'
        rows = self.get_table_rows('imagenes', 'filters[pagina.{}][eq]={}'.format(filter_by, pagina))
        # if not rows:
        #     raise Exception('No se han encontrado imágenes para la página ' + pagina)
        imgs = {}
        for row in rows:
            ubic = row['ubicacion'].split('-')
            ubicfmt = []
            for ubi in ubic:
                ubicfmt.append(ubi.strip().lower())
                if not ubicfmt[-1].isalnum():
                    raise Exception('El dato de ubicacion "{}" en la tabla de textos tiene caractéres inválidos'.format(ubicfmt[-1]))
            imgurl = self.img_row_to_url(row['imagen'], 'Hay una imagen vacía para la ubicacion "{}"'.format(row['ubicacion']))
            if len(ubic) == 1:
                imgs[ubicfmt[0]] = imgurl
            else:
                if ubicfmt[0] not in imgs:
                    imgs[ubicfmt[0]] = {}
                imgs[ubicfmt[0]][ubicfmt[1]] = imgurl
        return imgs

    def get_items(self, table, pagina, keys_types):
        if pagina:
            rows = self.get_table_rows(table, filter='filters[pagina.nombre][eq]={}'.format(pagina))
        else:
            rows = self.get_table_rows(table)
        items = []
        for row in rows:
            item = {}
            for key, type in keys_types.items():
                if type == DirectusApi.RowTypes.TEXT:
                    item[key] = row[key]
                elif type == DirectusApi.RowTypes.IMG:
                    item[key] = self.img_row_to_url(row[key], 'Un item de {} no tiene imagen asignada'.format(table))
                elif type == DirectusApi.RowTypes.DATETIME:
                    item[key] = datetime.datetime.strptime(row[key], "%Y-%m-%d %H:%M:%S")
                elif type == DirectusApi.RowTypes.REL_NOMBRE:
                    item[key] = row[key]['data']['nombre']
                else:
                    raise Exception('Tipo de dato inválido para columna {}'.format(key))
            items.append(item)
        return items

    def get_items_novedades(self, pagina):
        return self.get_items('items_novedades', pagina, {
                'ancho_columnas': DirectusApi.RowTypes.TEXT,
                'titulo': DirectusApi.RowTypes.TEXT,
                'hashtag': DirectusApi.RowTypes.TEXT,
                'imagen': DirectusApi.RowTypes.IMG
            })

    def get_items_agenda(self, pagina):
        return self.get_items('items_agenda', pagina, {
                'fechahora': DirectusApi.RowTypes.DATETIME,
                'titulo': DirectusApi.RowTypes.TEXT,
                'hashtag': DirectusApi.RowTypes.TEXT,
                'icono': DirectusApi.RowTypes.IMG
            })

    def get_items_propuestas(self):
        return self.get_items('items_propuestas', None, {
                'titulo': DirectusApi.RowTypes.TEXT,
                'texto': DirectusApi.RowTypes.TEXT,
                'icono': DirectusApi.RowTypes.IMG,
                'imagen_fondo': DirectusApi.RowTypes.IMG,
                'pagina': DirectusApi.RowTypes.REL_NOMBRE
            })

    def get_items_seguidor(self, pagina):
        return self.get_items('items_seguidor', pagina, {
                'titulo': DirectusApi.RowTypes.TEXT,
                'imagen': DirectusApi.RowTypes.IMG,
                'url': DirectusApi.RowTypes.TEXT
            })

    def get_items_tema(self, pagina):
        return self.get_items('items_tema', pagina, {
                'titulo': DirectusApi.RowTypes.TEXT,
                'texto': DirectusApi.RowTypes.TEXT,
                'imagen': DirectusApi.RowTypes.IMG
            })


dapi = DirectusApi()


def init_flask_app(directus_url_int, directus_url_ext, api_path, auth_token):
    global dapi
    dapi.init_api(directus_url_int, directus_url_ext, api_path, auth_token)
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
