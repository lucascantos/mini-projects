from apiclient.discovery import build
from httplib2 import Http
from oauth2client import client, tools
from oauth2client.file import Storage

class GoogleSlide(object):
    def __init__(self, client_secret_file, template_id):
        '''
        Cria  uma nova apresentação a partir de um template

        client_secret_file: arquivo de autenticação aos arquivos e dados do google API
        '''

        self.client_secret_file = client_secret_file
        self.template_id = template_id
        self.reqs = []



    def client_credenciais(self, token=False):
        '''
        Prepara as credenciais de acesso aos arquivos e documentos do google
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
            flow = client.flow_from_clientsecrets(client_path, scopes)
            self.credz = tools.run_flow(flow, store)

        # Cria os serviços de Drive e Slides        
        self.drive_services = build('drive', 'v3', http=self.credz.authorize(Http()))
        self.slides_services = build('slides', 'v1', http=self.credz.authorize(Http()))
        
        self.clone_presentation()


    def clone_presentation(self):
        #Cria uma copia do template pra ser alterado
        self.new_presentation = self.drive_services.files().copy(body={'name': 'Teste01'}, fileId = self.template_id).execute()

    def grab_template_element(self, object_name):
        '''
        Busca o elemento dentro dos templates e devolve o objeto
        '''
        slides = self.slides_services.presentations().get(presentationId = self.new_presentation['id'], fields = 'slides').execute().get('slides', [])
        for self.slide in slides:
            self.obj = None
            for self.obj in self.slide['pageElements']:
                text = self.obj['shape']['text']['textElements'][1]['textRun']['content']
                if text == object_name:
                    break

    def new_image(self, img_file, slide_obj):
        '''
        cria uma nova imagem no lugar de um objeto em especifico

        file_name: Nome do arquivo de imagem
        slide_obj: Objeto dentro do template que vai ser substitudo pela imagem
        '''

        self.grab_template_element(slide_obj)

        new_image = {'createImage': {
                        'url': img_file,
                        'elementProperties': {
                            'pageObjectId': self.slide['objectId'],
                            'size': self.obj['size'],
                            'transform': self.obj['transform'],
                        }
                    }}      
        self.reqs.append(new_image)

        self.reqs.append({'deleteObject': {'objectId': self.obj['objectId']}})

# Caminho pros arquivos de autencticação
client_path = 'GoogleAPI/credentials/client_secret.json'
service_path = './credentials/service_key.json'
template_id = '1k2NX5dV6KPoyMq89phXFQ_QoOyhti4Sc9Yw6oDX97Z4'

logo = {'file': 'logo.jpg', 'placeholder': '{{LOGO}}'}
meuslide = GoogleSlide(client_path, template_id)
meuslide.client_credenciais()

meuslide.new_image(logo['file'], logo['placeholder'])

print(meuslide.reqs)
