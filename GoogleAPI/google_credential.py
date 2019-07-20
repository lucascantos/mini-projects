from apiclient.discovery import build
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
    def __init__(self, client_secret_file, template_id):
        '''
        Cria  uma nova apresentação a partir de um template

        client_secret_file: arquivo de autenticação aos arquivos e dados do google API
        template_id: ID do GSlides de template para a criação. Pode pegar direto acessando no navegador
        '''

        self.client_secret_file = client_secret_file
        self.template_id = template_id

        # Lista de requests que vai ser usado pra montar os slides
        self.reqs = []

    def client_credenciais(self, token=False):
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

        # Cria os serviços de Drive e Slides        
        self.drive_services = build('drive', 'v3', http=self.credz.authorize(Http()))
        self.slides_services = build('slides', 'v1', http=self.credz.authorize(Http()))

    def grab_file_drive(self, img_file_name):
        '''
        Busca arquivo de imagem dentro do GDrive e devolve a URL deste        
        img_file_name: nome do arquivo de imagem
        '''
        # cria um link com acesso ao logo de imagem que vc quer
        template_file = self.drive_services.files().list(q = "name='{}'".format(img_file_name)).execute()['files'][0]
        id_uri = self.drive_services.files().get_media(fileId=template_file['id']).uri
        credz_token = self.credz.access_token
        return ('{}&access_token={}'.format(id_uri, credz_token))
