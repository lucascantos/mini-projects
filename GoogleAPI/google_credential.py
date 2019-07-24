from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import client, tools
from oauth2client.file import Storage


def error_handler(function):
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except Exception as e:
            print(e)
            return None
    return wrapper

class GoogleDrive(object):
    def __init__(self, client_secret_file):
        '''
        Prepara credenciais à uma conta Google e acessa o Drive
        client_secret_file: arquivo de autenticação aos arquivos e dados do google API
        '''
        self.client_secret_file = client_secret_file
        self._client_credenciais()
        
    @error_handler
    def _client_credenciais(self, token=False):
        '''
        Prepara as credenciais de acesso aos arquivos e documentos do google
        token: Por enquanto inutil. A ideia é que a autorização pode ser via Token ou via Credencial
        '''
        scopes = [
                'https://www.googleapis.com/auth/spreadsheets.readonly',
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/presentations'
                ]
        # esse Storage é criado, se não existir, pra não ter que ficar toda hora pedindo permissão
        store = Storage('GoogleAPI/credentials/storage.json')
        self.credz = store.get()
        if not self.credz or self.credz.invalid:
            flow = client.flow_from_clientsecrets(self.client_secret_file, scopes)
            self.credz = tools.run_flow(flow, store)

        # Cria os serviços de Drive e Slides. Por hora, criando todas aqui, mas o ideal é separa-las     
        self.drive_services = build('drive', 'v3', http=self.credz.authorize(Http()))
        self.slides_services = build('slides', 'v1', http=self.credz.authorize(Http()))
        self.sheet_services = build('sheets', 'v4', http=self.credz.authorize(Http()))
    
    def _get_fileid (self, file_name, mimeType=''):
        '''
        Converte uma string com nome de um arquivo na conta google para o ID dele.
        file_name: nome do arquivo no drive, sheets ou slides
        '''
        query_string = f"name='{file_name}'"
        if mimeType != '':
            query_string = f"{query_string} and mimeType='{mimeType}'"
        return self.drive_services.files().list(q=query_string).execute()['files'][0]

    def _file_to_url(self, img_file_name):
        '''
        Busca arquivo de imagem dentro do GDrive e devolve a URL deste        
        img_file_name: nome do arquivo de imagem
        '''
        # cria um link com acesso ao logo de imagem que vc quer
        template_file = self._get_fileid(img_file_name)
        id_uri = self.drive_services.files().get_media(fileId=template_file['id']).uri
        credz_token = self.credz.access_token
        return ('{}&access_token={}'.format(id_uri, credz_token))
    
    def upload_file(self, local_path):
        '''
        Faz upload de arquivo local para o Google Drive.
        local_path: string, caminha do arquivo pra upload. Não funciona URL.

        Documentação do MediaFileDownload
        https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.http.MediaFileUpload-class.html
        '''
        folder_mimeType = 'application/vnd.google-apps.folder'
        folder_id = self._get_fileid('Imagens', mimeType=folder_mimeType)
        image_metadata = {
            'name': 'teste',
            'parents': [folder_id['id']]
        }
        media = MediaFileUpload(local_path, mimetype='image/jpeg')
        self.drive_services.files().create(media_body=media, fields='id', body=image_metadata).execute()