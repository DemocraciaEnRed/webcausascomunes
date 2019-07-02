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
    def __init__(self):
        self.ser_url = None
        self.api_url = None
        self.token = None
        self.auth_header = None
        self.textosregx = re.compile('^[^<>&]*$')

    def init_api(self, ser_url, api_path, token):
        if not ser_url[-1] == '/':
            ser_url += '/'
        if api_path[0] == '/':
            api_path = api_path[1:]
        self.ser_url = ser_url
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
            raise Exception('El servidor directus devolvió {} al comando {}'.format(r.status_code, api_cmd))
        if r.text == 'You must be logged in to access the API':
            raise Exception('Mala autenticación al servidor directus')
        try:
            rj = r.json()
        except ValueError:
            raise Exception('El servidor directus devolvió un json inválido al comando ' + api_cmd)
        return rj

    def test_conn(self):
        r = requests.get(self.ser_url + 'server/ping')
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

    def get_textos(self, pagina):
        pagina = str(pagina)
        if str.isnumeric(pagina):
            filter_by = 'id'
        else:
            filter_by = 'nombre'
        rows = self.get_table_rows('textos', 'filters[pagina.{}][eq]={}'.format(filter_by, pagina))
        if not rows:
            raise Exception('No se han encontrado textos para la página ' + pagina)
        textos = {}
        for row in rows:
            ubic = row['ubicacion'].split('-')
            ubicfmt = []
            for ubi in ubic:
                ubicfmt.append(ubi.strip().lower())
                if not ubicfmt[-1].isalnum():
                    raise Exception('El dato de ubicacion "{}" en la tabla de textos tiene caractéres inválidos'.format(ubicfmt[-1]))
            txt = row['texto']
            if self.textosregx.match(txt) is None:
                raise Exception('El dato de texto "{}" en la tabla de textos tiene caractéres inválidos'.format(txt))
            if len(ubic) == 1:
                textos[ubicfmt[0]] = txt
            else:
                if ubicfmt[0] not in textos:
                    textos[ubicfmt[0]] = {}
                textos[ubicfmt[0]][ubicfmt[1]] = txt
        return textos

    def get_imgs(self, pagina):
        pagina = str(pagina)
        if str.isnumeric(pagina):
            filter_by = 'id'
        else:
            filter_by = 'nombre'
        rows = self.get_table_rows('imagenes', 'filters[pagina.{}][eq]={}'.format(filter_by, pagina))
        if not rows:
            raise Exception('No se han encontrado imágenes para la página ' + pagina)
        imgs = {}
        for row in rows:
            ubic = row['ubicacion'].split('-')
            ubicfmt = []
            for ubi in ubic:
                ubicfmt.append(ubi.strip().lower())
                if not ubicfmt[-1].isalnum():
                    raise Exception('El dato de ubicacion "{}" en la tabla de textos tiene caractéres inválidos'.format(ubicfmt[-1]))
            img = row['imagen']
            if not img:
                raise Exception('Hay una imagen vacía para la ubicacion "{}"'.format(row['ubicacion']))
            imgurl = self.ser_url + img['data']['url']
            if len(ubic) == 1:
                imgs[ubicfmt[0]] = imgurl
            else:
                if ubicfmt[0] not in imgs:
                    imgs[ubicfmt[0]] = {}
                imgs[ubicfmt[0]][ubicfmt[1]] = imgurl
        return imgs

    def get_itemsnovedades(self):
        rows = self.get_table_rows('items_novedades')
        items = []
        for row in rows:
            if not row['imagen']:
                raise Exception('Un item de novedades no tiene imagen asignada')
            imgurl = row['imagen']['data']['url']
            item = {
                'ancho_columnas': row['ancho_columnas'],
                'titulo': row['titulo'],
                'hashtag': row['hashtag'],
                'imgurl': self.ser_url + imgurl
            }
            items.append(item)
        return items

    def get_itemsagenda(self):
        rows = self.get_table_rows('items_agenda')
        items = []
        for row in rows:
            item = {
                'fechahora': datetime.datetime.strptime(row['fecha'], "%Y-%m-%d %H:%M:%S"),
                'titulo': row['titulo'],
                'hashtag': row['hashtag']
            }
            items.append(item)
        return items


dapi = DirectusApi()


def init_flask_app(directus_url, api_path, auth_token):
    global dapi
    dapi.init_api(directus_url, api_path, auth_token)
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
