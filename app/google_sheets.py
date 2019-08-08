#  Python Quickstart - https://developers.google.com/sheets/api/quickstart/python


class GSheetApi:
    def __init__(self, app):
        self.authenticated = False
        self.client_id = app.config.get('GSHEETS_CLIENT_ID')
        self.project_id = app.config.get('GSHEETS_PROJECT_ID')
        self.client_secret = app.config.get('GSHEETS_CLIENT_SECRET')
        self.sheet_id = app.config.get('GSHEETS_SHEET_ID')
        self.service = None

    def authenticate(self):
        import os.path
        import pickle
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request

        creds = None

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                import json
                json_config = json.loads(f'''{{"installed":
                  {{"client_id":"{self.client_id}",
                    "project_id":"{self.project_id}",
                    "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                    "token_uri":"https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret":"{self.client_secret}",
                    "redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]
                  }}
                }}''')

                # If modifying these scopes, delete the file token.pickle.
                scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
                flow = InstalledAppFlow.from_client_config(json_config, scopes)
                # flow = InstalledAppFlow.from_client_secrets_file(jsonfile, scopes)

                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)
        self.authenticated = True

    def get_rows(self):
        rows = []

        # Call the Sheets API
        sheet = self.service.spreadsheets()
        read_start = 14
        read_length = 10
        read_last = read_start
        while True:
            read_range = f'A{read_last}:I{read_last+read_length}'
            result = sheet.values().get(spreadsheetId=self.sheet_id, range=read_range).execute()
            values = result.get('values')
            if not values:
                break
            else:
                rows.extend(values)
                read_last += read_length

        return rows
