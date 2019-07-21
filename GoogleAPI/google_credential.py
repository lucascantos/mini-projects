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

        # Cria os serviços de Drive e Slides. Por hora, criando todas aqui, mas o ideal é separa-las     
        self.drive_services = build('drive', 'v3', http=self.credz.authorize(Http()))
        self.slides_services = build('slides', 'v1', http=self.credz.authorize(Http()))
        self.sheet_services = build('sheets', 'v4', http=self.credz.authorize(Http()))
    
    def get_fileid (self, file_name, mimeType=''):
        '''
        Converte uma string com nome de um arquivo na conta google para o ID dele.
        file_name: nome do arquivo no drive, sheets ou slides
        '''
        query_string = f"name='{file_name}'"
        if mimeType != '':
            query_string = f"{query_string} and mimeType='{mimeType}'"
        return self.drive_services.files().list(q=query_string).execute()['files'][0]

    def grab_file_drive(self, img_file_name):
        '''
        Busca arquivo de imagem dentro do GDrive e devolve a URL deste        
        img_file_name: nome do arquivo de imagem
        '''
        # cria um link com acesso ao logo de imagem que vc quer
        template_file = self.get_fileid(img_file_name)
        id_uri = self.drive_services.files().get_media(fileId=template_file['id']).uri
        credz_token = self.credz.access_token
        return ('{}&access_token={}'.format(id_uri, credz_token))
    
    def upload_image(self, local_path):
        '''
        Faz upload de arquivo local para o Google Drive.
        local_path: string, caminha do arquivo pra upload. Não funciona URL.

        Documentação do MediaFileDownload
        https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.http.MediaFileUpload-class.html
        '''
        folder_mimeType = 'application/vnd.google-apps.folder'
        folder_id = self.get_fileid('Imagens', mimeType=folder_mimeType)
        image_metadata = {
            'name': 'teste',
            'parents': [folder_id['id']]
        }
        media = MediaFileUpload(url, mimetype='image/jpeg')
        self.drive_services.files().create(media_body=media, fields='id', body=image_metadata).execute()

    def crop_image(self):
        '''
        Esse metodo deve ir pro Image Graber
        '''
        import cv2
        import urllib.request        
        import numpy as np

        with urllib.request.urlopen(target_image) as url:
            resp = url.read()
        image = np.asarray(bytearray(resp), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        img = cv2.imread(local_image)

    def pdf_slicer(self):
        from PyPDF2 import PdfFileReader, PdfFileWriter
        from PIL import Image
        import requests
        from io import StringIO, BytesIO
        import urllib.request

        target_image = 'https://i.kym-cdn.com/photos/images/original/000/124/933/1304376955947.png'
        target_pdf = 'https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/lanina/enso_evolution-status-fcsts-web.pdf'
        local_pdf = 'GoogleAPI\enso_evolution-status-fcsts-web.pdf'

        # with urllib.request.urlopen(target_pdf) as url:
        #     resp = url.read()
        x = requests.get(target_pdf)

        # page = convert_from_bytes(resp, 12)
        # print(page)
        # print(x.content)
        url_encoded = BytesIO(x.content)
        pdf = open(url, 'rb')
        fileReader = PdfFileReader(BytesIO(x.content))
        page0 = fileReader.getPage(4)
        print(page0)

        xObject = page0['/Resources']['/XObject'].getObject()
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                if size[0] < 2000 and size[1] > 149:
                    try: 
                        data = xObject[obj].getData()
                        if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                            mode = "RGB"
                        else:
                            mode = "P"
                        
                        if '/Filter' in xObject[obj]:
                            if xObject[obj]['/Filter'] == '/FlateDecode':
                                img = Image.frombytes(mode, size, data)
                                img.save(obj[1:] + ".png")
                            elif xObject[obj]['/Filter'] == '/DCTDecode':
                                img = open(obj[1:] + ".jpg", "wb")
                                img.write(data)
                                img.close()
                            elif xObject[obj]['/Filter'] == '/JPXDecode':
                                img = open(obj[1:] + ".jp2", "wb")
                                img.write(data)
                                img.close()
                            elif xObject[obj]['/Filter'] == '/CCITTFaxDecode':
                                img = open(obj[1:] + ".tiff", "wb")
                                img.write(data)
                                img.close()
                        else:
                            img = Image.frombytes(mode, size, data)
                            img.save(obj[1:] + ".png")
                        
                        print(obj, size)
                    except:
                        print(f'Error: {obj}')
                        pass

        print('Good')
    