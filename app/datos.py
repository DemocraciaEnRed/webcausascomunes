import csv
# import json
# import io

#https://docs.google.com/spreadsheets/d/1xsr1szDVCsgl7UfJMv6mGaDiVObtd_FqFJHHs4qwDIM
presu_headers = ('fecha', 'importe', 'categoria', 'concepto', 'descripcion', 'proveedor', 'tipo de comprobante',
           'forma de pago', 'original')

def get_presu_headers():
    return presu_headers

def get_cols_from_csv(csv_path):
    # jsonfile = io.StringIO('')

    csvfile = open(csv_path, 'r')
    cols = {}
    for h in presu_headers:
        cols[h] = []
    reader = csv.DictReader(csvfile, presu_headers)
    for row in reader:
        for h in presu_headers:
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
        rows.append(row)

    return rows
