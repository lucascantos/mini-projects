from apiclient.discovery import build
from httplib2 import Http
from oauth2client import client, tools
from oauth2client.file import Storage

def discovery_google():
        start = 'https://developers.google.com/api-client-library/python/'
        # pip install --upgrade google-api-python-client
        # pip install oauth2client
        hue = 'https://developers.google.com/apis-explorer/#p/discovery/v1/discovery.apis.getRest'

def api_key():
        # on build, use developerKey = 
        key = ''
        return key

def client_credenciais(token=False):
        # on build, use http = 
        scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/presentations'
                ]
        # Caminho pros arquivos de autencticação
        client_path = 'GoogleAPI/credentials/client_secret.json'
        service_path = './credentials/service_key.json'

        # esse Storage é criado, se não existir, pra não ter que ficar toda hora pedindo permissão
        store = Storage('storage.json')
        credz = store.get()
        if not credz or credz.invalid:
                flow = client.flow_from_clientsecrets(client_path, scopes)
                credz = tools.run_flow(flow, store)
        if token:
                return credz
        else:
                return credz.authorize(Http())

# Google drive
# simple list of files on my google drive
def drive_google():
        '''
        https://developers.google.com/drive/api/v3/search-files
        '''

        drive_service = build('drive', 'v3', http=client_credenciais())
        query = {'q': 'name="logo.jpg"'}
        query2 = {'q': "mimeType='application/vnd.google-apps.spreadsheet'"}
        files = drive_service.files().list(q = "name='logo.jpg'")
        files = files.execute().get('files', [])
        for f in files:
                print (f['name'], f['mimeType'])

# Google Sheets
# Simple listing of a sheets data
def sheets_google():
        '''
        https://developers.google.com/sheets/api/reference/rest/
        https://developers.google.com/sheets/api/samples/
        '''
        my_sheet = {'id': '1Bia3UOHA8aT49dap7RinFXB3uiH5eufcp3Djf_eT8bk', 'name': 'Redecs e Mar'}
        sheets_service = build('sheets', 'v4', http=client_credenciais())
        sheet = sheets_service.spreadsheets().values().get(
                spreadsheetId='1Bia3UOHA8aT49dap7RinFXB3uiH5eufcp3Djf_eT8bk',
                range="Página1",
                majorDimension='COLUMNS')
        sheet = sheet.execute()

        sheet_data = sheets_service.spreadsheets().get(spreadsheetId=my_sheet['id'])
        sheet_data = sheet_data.execute()
        print(sheet['values'])


def slides_google():
        slide = 'MeuSlide'
        logo_file = 'logo.jpg'
        drive_service = build('drive', 'v3', http=client_credenciais())
        slides_service = build('slides', 'v1', http=client_credenciais())

        template_file = drive_service.files().list(q = "name='%s'" % slide).execute()['files'][0]
        data = {'name': 'Google Slides API DEMO'}
        deck_file = drive_service.files().copy(body=data, fileId=template_file['id']).execute()['id']

        slides = slides_service.presentations().get(presentationId = deck_file, fields = 'slides').execute().get('slides', [])[0]
        obj = None
        for obj in slides['pageElements']:
                if obj['shape']['shapeType'] == 'RECTANGLE':
                        break

        # cria um link com acesso ao logo de imagem que vc quer
        template_file = drive_service.files().list(q = "name='{}'".format(logo_file)).execute()['files'][0]
        id_uri = drive_service.files().get_media(fileId=template_file['id']).uri
        credz_token = client_credenciais(token=True).access_token
        img_url = '{}&access_token={}'.format(id_uri, credz_token)

        # Altera os placeholders do slide
        # lista de requests https://developers.google.com/slides/reference/rest/v1/presentations/response#Response
        reqs = [
                {'replaceAllText': {'replaceText': 'Hello World!', 'containsText': {'text': '{{NAME}}'}}},
                {'createImage': {
                        'url': img_url,
                        'elementProperties': {
                                'pageObjectId': slides['objectId'],
                                'size': obj['size'],
                                'transform': obj['transform'],
                        }
                }},
                {'deleteObject': {'objectId': obj['objectId']}},
        ]

        slides_service.presentations().batchUpdate(body={'requests': reqs}, presentationId=deck_file, fields='').execute()
    
slides_google()
