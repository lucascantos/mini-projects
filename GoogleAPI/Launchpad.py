from apiclient.discovery import build
from httplib2 import Http
from oauth2client import client, tools
from oauth2client.file import Storage


def api_key():
    # on build, use developerKey = 
    key = 'AIzaSyC81Oi0aby8CIzSfdJJ3UWH2Gn4PbHYt3U '
    return key

def client_credenciais ():
    # on build, use http = 
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly']

    client_path = 'GoogleAPI\client_secret.json'
    service_path = 'GoogleAPI\LucasTest01-9b2076520c24.json'
        
    store = Storage('storage.json')
    credz = store.get()
    if not credz or credz.invalid:
        flow = client.flow_from_clientsecrets(client_path, scopes)
        credz = tools.run_flow(flow, store)
    return credz.authorize(Http())

# Google drive

service = build('drive', 'v3', http=client_credenciais())
files = service.files().list().execute().get('files', [])
print('YEET')
print(files)

for f in files:
    print (f['name'], f['mimeType'])

