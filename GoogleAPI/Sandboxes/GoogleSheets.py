'''
https://developers.google.com/api-client-library/python/start/get_started
https://www.youtube.com/watch?v=h-gBeC9Y9cE&list=PLOU2XLYxmsILOIxBRPPhgYbuSslr50KVq&index=3
Simple API (Books) = API key
Installed Aplications (Calendar) = client_secrets
Web Applocation


Motivos pra não dar certo:
    -tem que fechar ou deslogar da conta google pra ele logar denovo e mandar uma requisição
    -Quando usar flow, é necessario pegar o link bonitinho e colocar na credencial de cliente
É possivel fazer tudo isso sem esse flow e ter que montar um serviço local?
'''
from apiclient.discovery import build
from httplib2 import Http

from oauth2client import  tools
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow

from google_auth_oauthlib.flow import InstalledAppFlow


scopes = ['https://www.googleapis.com/auth/spreadsheets']
spread_sheet = {'id': '1Bia3UOHA8aT49dap7RinFXB3uiH5eufcp3Djf_eT8bk', 'name': 'Redecs e Mar'}
client_path = 'GoogleAPI\client_secret.json'
service_path = 'GoogleAPI\LucasTest01-9b2076520c24.json'

flow = InstalledAppFlow.from_client_secrets_file(client_path, scopes)
credentials = flow.run_local_server(host='localhost',
    port=8080, 
    authorization_prompt_message='Please visit this URL: {url}', 
    success_message='The auth flow is complete; you may close this window.',
    open_browser=True)

service = build('sheets', 'v3', credentials=credentials)
sheet = service.spreadsheet
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=SAMPLE_RANGE_NAME).execute()
values = result.get('values', [])

'''
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
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
            print('%s, %s' % (row[0], row[4]))

if __name__ == '__main__':
    main()
'''

'''


import gspread
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials

# Achar o Scope da API

img_file = ''
template_slide = ''

scope = ['https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/presentations']

store = file.Storage('GoogleAPI\storage.json')
creds = store.get()


credentials = ServiceAccountCredentials.\
    from_json_keyfile_name('GoogleAPI\storage.json', scope)

if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets('GoogleAPI\client_secret.json', scope)
    credentials = tools.run_flow(flow, store)

sheets = build('sheets', 'v4', credentials=credentials.authorize(Http()))

------------------------

credentials = ServiceAccountCredentials.\
    from_json_keyfile_name('service_credentials.json', scope)

client = gspread.authorize(credentials)

sheet = client.open('Redecs e Mar').sheet1
data = sheet.get_all_records()
data = sheet.row_values(3)

sheet.update_cell(1, 4, 'AAAA')

new_row = ['AAA', 'BBB']
index = 1
sheet.insert_row(new_row, index)

print(data)
'''