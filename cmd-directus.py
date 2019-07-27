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


pags = {}
def load_pags():
    pag_rows = api_get('tables/paginas/rows')
    for p in pag_rows:
        pags[p['nombre'].lower()] = p['id']


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

    print(api_txt_add(pag_id, ubi_arg, txt_arg, fmt_arg))

else:
    ret_err(f'Comando "{cmd}" inválido. Solo válidos: txtlocked, txtlock, txtunlock, getpags, txtadd')
