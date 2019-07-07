from apiclient.discovery import build
from httplib2 import Http
from oauth2client import client, tools
from oauth2client.file import Storage
from pprint import pprint
import uuid

def error_handler(function):
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except Exception as e:
            print(e)
            return None
    return wrapper

class GoogleSlide(object):
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

    @error_handler
    def push_change(self):
        self.slides_services.presentations().batchUpdate(body={'requests': self.reqs}, presentationId=self.new_presentation['id'], fields='').execute()
        self.reqs = []

    def grab_image(self, img_file_name):
        '''
        Busca arquivo de imagem dentro do GDrive e devolve a URL deste
        
        img_file_name: nome do arquivo de imagem
        '''
        # cria um link com acesso ao logo de imagem que vc quer
        template_file = self.drive_services.files().list(q = "name='{}'".format(img_file_name)).execute()['files'][0]
        id_uri = self.drive_services.files().get_media(fileId=template_file['id']).uri
        credz_token = self.credz.access_token
        return ('{}&access_token={}'.format(id_uri, credz_token))

    def add_image(self, img_file, slide_obj):
        '''
        cria uma nova imagem no lugar de um objeto em especifico

        param file_name: Nome do arquivo de imagem
        param slide_obj: Objeto dentro do template que vai ser substitudo pela imagem
        '''

        
        img_url = self.grab_image(img_file)
        for _ in self.grab_template_element(slide_obj):
            new_image = {'createImage': {
                            'url': img_url,
                            'elementProperties': {
                                'pageObjectId': self.slide['objectId'],
                                'size': self.obj['size'],
                                'transform': self.obj['transform'],
                            }
                        }}
            self.reqs.append(new_image)
            self.reqs.append({'deleteObject': {'objectId': self.obj['objectId']}})

    def add_text(self, text, slide_obj):
        '''
        Substitui todos os textos com aquele ID no texto.

        text: Texto que será inserido
        slide_obj: Texto que será substituido
        '''
        new_text =  {'replaceAllText': {'replaceText': text, 'containsText': {'text': slide_obj}}}
        self.reqs.append(new_text)

    def grab_template_element(self, object_name):
        '''
        METODO 1
        Busca o elemento dentro dos templates e devolve o objeto
        '''
        self.slides = self.slides_services.presentations().get(presentationId = self.new_presentation['id'], fields = 'slides').execute().get('slides', [])
        self.obj = None
        for self.slide in self.slides:
            for self.obj in self.slide['pageElements']:
                try:
                    text = self.obj['shape']['text']['textElements'][1]['textRun']['content'][:-1]
                    if text == object_name:
                        yield
                except:
                    print('Esse elemento não possui texto!')

    def clone_presentation(self, name):
        '''
        METODO 1
        Cria uma copia do template pra ser alterado.
        Valide para o caso de ter um template completo de uma apresentação
        '''
        old_slide = self.drive_services.files().list(q = 'name="{}"'.format(name)).execute()['files'][0]

        if old_slide:
            # Deleta slides antigos com o mesmo nome só pra não explodir meu driver
            self.drive_services.files().delete(fileId=old_slide['id']).execute()
        self.new_presentation = self.drive_services.files().copy(body={'name': 'Teste01'}, fileId = self.template_id).execute()

    def create_presentation(self, name):
        '''
        De um arquivo de templates, ele pega apenas um dos slides e copia este para o novo
        name: Nome da nova apresentação, ou apresentação existente
        '''
        # Try Abrir novo slides
        # Except Criar novo slides
        try:
            self.new_presentation = self.drive_services.files().list(q = 'name="{}"'.format(name)).execute()['files'][0]
            print("Slide existente")
        except:
            body={
                'title': name
            }
            self.slides_services.presentations().create(body=body).execute()
            self.new_presentation = self.drive_services.files().list(q = 'name="{}"'.format(name)).execute()['files'][0]

            print("Novo Slide Criado")
    
        # Abrir o template
        self.template_file = self.slides_services.presentations().get(presentationId = self.template_id).execute()
        self.slides_labeler()

    def slides_labeler(self):
        '''
        cria uma lista com os labels e ids dos slides. 
        necessario, pois não tem um jeito simples de diferenciar entre os slides
        imagino que tenha como otimizar isso aki
        '''
        self.slide_list=[]
        for slide in self.template_file['slides']:
            slide_id = slide['objectId']
            for element in slide['pageElements']:
                if element['shape']['shapeType'] == 'ELLIPSE':
                    slide_label = element['shape']['text']['textElements'][1]['textRun']['content']
                    self.slide_list.append({'id': slide_id, 'label': slide_label, 'newId': str(uuid.uuid4())})

    def add_slide(self, slide_label):
        '''
        Adiciona novo slide à apresentação.
        slide_label: nome do slide dado no template, dentro de uma eslipse
        '''
        # pega o slide_label
        for slide_props in self.slide_list:
            if slide_props['label'][:-1]==slide_label:
                break

        # usa o label pra pegar o id
        # pega slide com aquele id e copia os Elementos
        for template_slide in self.template_file['slides']:
            if template_slide['objectId'] == slide_props['id']:
                slide_elements = template_slide['pageElements']
                break

        # cria um novo slide na nova apresentação com ess lista de elementos
        new_slide_request = {
            'createSlide': {'objectId': slide_props['newId']}
        }
        self.reqs.append(new_slide_request)


        for index, slide_element in enumerate(slide_elements):
            self.get2create(slide_element, slide_props['newId'], index)



    def get2create(self, slide_element, slide_id, index):
        '''
        Converte o JSON de get pra um JSON de create.
        '''
        create_shape = {'createShape': {
            'objectId': '{}_{}'.format(slide_id, index),
            'shapeType': slide_element['shape']['shapeType'],
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': slide_element['size'],
                'transform': slide_element['transform']
            },
        }}

        insert_text = {'insertText': {
            'objectId': '{}_{}'.format(slide_id, index),
            'text': slide_element['shape']['text']['textElements'][1]['textRun']['content']
        }}

        update_text_style = {'updateTextStyle': {
          'objectId': '{}_{}'.format(slide_id, index),
          'fields': '*',
          'style': slide_element['shape']['text']['textElements'][1]['textRun']['style']
        }}

        update_paragraph_style = {
            'updateParagraphStyle': {
                'objectId': '{}_{}'.format(slide_id, index),
                'fields': '*',
                'style': slide_element['shape']['text']['textElements'][0]['paragraphMarker']['style']
            }}

        self.reqs.append(create_shape)
        self.reqs.append(insert_text)
        self.reqs.append(update_text_style)
        self.reqs.append(update_paragraph_style)

    def clear_labels(self):
        # remove objetos de label dos slides
        pass
    
    @error_handler
    def template_builder(id):
        pass
        # Abrir referencia
        example_slides = self.slides_services.presentations().get(presentationId = id, fields = 'slides').execute().get('slides', [])
        # pra cada slide LOOP
        # pra cada elemento LOOP
        for slide in template_slides:
            for element in slide:
                print(element)
        
                
        # SE elemento = imagem
        # pegar size e transformada do elemento
        # criar retangulos com essa propriedade
        # SE elemento = texto
        # copiar elemento pro novo slide
        # OU
        # criar um elemento de texto apenas com size/transform
        # SE elemento = graph
        # pass
        # SE elemento = tabela
        # pass