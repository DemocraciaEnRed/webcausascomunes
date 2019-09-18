import csv

class Dataset:    
    def get_rendered_headers(self):
        rendered_headers = [h for h in self.csv_headers if h not in self.exclude_headers]
        return rendered_headers    
    
    def get_rows_from_csv(self):
        csvfile = open(self.csv_path, 'r')
        reader = csv.reader(csvfile, delimiter=',')
    
        # saltear encabezados
        next(reader)
    
        return self._exclude_columns(reader)
    
    
    def get_rows_from_gsheet(self, gsheet_api):
        if not gsheet_api.authenticated:
            gsheet_api.authenticate()
    
        raw_rows = gsheet_api.get_rows()
    
        
        return self._exclude_columns(raw_rows) if len(self.exclude_headers) else raw_rows

    def _exclude_columns(self, rows_iterable):
        rows = []
    
        # sorteado en reverse así deleteamos desde el último al primero
        # sino se irían corriendo los indices a medida que borramos
        exclude_headers_i = sorted([self.csv_headers.index(h) for h in self.exclude_headers], reverse=True)
        for row in rows_iterable:
            for exclude_header_i in exclude_headers_i:
                # puede suceder que una fila contenga menos campos,
                # entonces del tiraría error (out of index range)
                if exclude_header_i < len(row):
                    del row[exclude_header_i]
            rows.append(row)
    
        return rows
    

class Cuentas(Dataset):
    def __init__(self, csv_path):
        # csv original - https://docs.google.com/spreadsheets/d/1ln55tuBltKipY5LDTEjRO6Fv79xLLK6COzfVu8ItX8I/edit#gid=0
        self.csv_path = csv_path
        self.csv_headers = ('fecha', 'importe', 'categoria', 'concepto', 'descripcion', 'proveedor',
                   'tipo de comprobante', 'forma de pago', 'original')
        self.exclude_headers = {'proveedor', 'original'}



class Colaboraciones(Dataset):
    def __init__(self, csv_path):
        # csv original - https://docs.google.com/spreadsheets/d/1zVvDW0PCRWkcYpLbfqYD8O_kWklgFPvIxU5JMSoPe0k/edit#gid=0
        self.csv_path = csv_path
        self.csv_headers = ('fecha', 'aportante', 'tipo', 'tiempo', 'destino', 'descripcion')
        self.exclude_headers = set()



'''# import json
# import io
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

    return cols'''
