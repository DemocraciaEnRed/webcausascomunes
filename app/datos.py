import csv
# import json
# import io

# csv original - https://docs.google.com/spreadsheets/d/1xsr1szDVCsgl7UfJMv6mGaDiVObtd_FqFJHHs4qwDIM
csv_headers = ('fecha', 'importe', 'categoria', 'concepto', 'descripcion', 'proveedor',
               'tipo de comprobante', 'forma de pago', 'original')

exclude_headers = {'proveedor', 'original'}
exclude_headers_i = sorted([csv_headers.index(h) for h in exclude_headers], reverse=True)

rendered_headers = [h for h in csv_headers if h not in exclude_headers]


def get_rendered_headers():
    return rendered_headers


def get_cols_from_csv(csv_path):
    # jsonfile = io.StringIO('')

    cols = {}
    for h in rendered_headers:
        cols[h] = []

    csvfile = open(csv_path, 'r')
    reader = csv.DictReader(csvfile, csv_headers)
    for row in reader:
        for h in rendered_headers:
            cols[h].append(row[h])
        # json.dump(row, jsonfile)
        # jsonfile.write('\n')
    # jsonfile.seek(0)

    return cols


def get_rows_from_csv(csv_path):
    csvfile = open(csv_path, 'r')
    reader = csv.reader(csvfile, delimiter=',')

    # saltear encabezados
    next(reader)

    rows = []
    for row in reader:
        for ex_h_i in exclude_headers_i:
            del row[ex_h_i]
        rows.append(row)

    return rows
