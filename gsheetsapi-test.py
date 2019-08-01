from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1ln55tuBltKipY5LDTEjRO6Fv79xLLK6COzfVu8ItX8I'
SAMPLE_RANGE_NAME = 'A13:I20'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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
            GSHEETS_CLIENT_ID = "501759720483-gn6a26gprv3tkk73qk5admsrt1l1pkr7.apps.googleusercontent.com"
            GSHEETS_PROJECT_ID = "quickstart-1563997715100"
            GSHEETS_CLIENT_SECRET = "RckfIm91JvE38evQGBI5mNAL"
            GSHEETS_SHEET_ID = "1ln55tuBltKipY5LDTEjRO6Fv79xLLK6COzfVu8ItX8I"
            import io
            jsonfile = io.StringIO('')
            jsonfile.write(f'''{{"installed":
              {{"client_id":"{GSHEETS_CLIENT_ID}",
                "project_id":"{GSHEETS_PROJECT_ID}",
                "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                "token_uri":"https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                "client_secret":"{GSHEETS_CLIENT_SECRET}",
                "redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]
              }}
            }}''')
            jsonfile.seek(0)
            flow = InstalledAppFlow.from_client_secrets_file(
                jsonfile, SCOPES)
            # esta línea te pide validación
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)

if __name__ == '__main__':
    main()