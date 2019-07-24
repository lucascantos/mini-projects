from google_sheets import GoogleSheets
import urllib.request
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image
import requests
from io import StringIO, BytesIO
import urllib.request

# Pega variaveis do link 
class UrlMaker(GoogleSheets):
    '''
    TODO: 
    Checar a variavel image_name pra ver se tem parametro no meio
    Otimizar o metodo split_param
    Otimizar a busca da variavel de HORA que vai na URL
    '''
    def __init__(self,client_secret_file):
        '''
        Classe que faz o download de uma imagem baseado no nome de uma variavel
        image_name: string, nome da variavel de referencia
        param: string, parametro extra opcional. (nome de cidade ou numero do mapa) (por hora, admite-se que só há 1 parametro extra)
        '''
        self.today_date = datetime.utcnow()
        super().__init__(client_secret_file)
        
    def grab_url(self, image_name, input_param=''):
        '''
        Busca dentro do banco de dados a linha que contem os dados.
        '''
        self.image_name = image_name
        self.input_param = input_param
        data_row = self.dataframe.loc[self.dataframe['name'] == self.image_name]
        self.url = data_row.iloc[0]['file_url']
        if data_row.iloc[0]['timedelta'] != '':
            timedelta = re.split(",", data_row.iloc[0]['timedelta'])
            self.time = [self._change_time(delta) for delta in timedelta]
        self._split_param()


        
    def _split_param(self):
        '''
        Busca dentro da string URL por parametro entre {}.
        conta quantas vezes a variavel ja foi chamada e chama a data correspondente
        '''
        reference_list = []
        param_object = '\{(.*?)\}'
        param_list = re.findall(param_object, self.url)
        for param in param_list:
            i = reference_list.count(param)
            if re.search('%', param):
                if param == '%H':
                     replacement = self._hour_default()
                else:
                    replacement = self.time[i].strftime(param)               
            else:
                if self.input_param == '':
                    self.input_param = input(f'Falta um parametro: {param}')
                replacement = str(self.input_param)
            
            self.url = self.url.replace('{'+param+'}', replacement)
            reference_list.append(param)

    def _hour_default(self):
        if self.today_date.hour >= 12:
            return '12'
        else:
            return '00'

    def _change_time(self, full_delta):
        '''
        função que converte o timedelta em data
        '''
        delta = int(full_delta[-2:])
        period = full_delta[:-2]
        keydelta = {period: delta}
        return self.today_date + relativedelta(**keydelta)
    
    def _crop_image(self):
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

        print('Good')
    

    def pdf_slicer(self):
        '''
        Extrai imagem de dentro de um pdf
        '''
        try:
            x = requests.get(self.url)
        except:
            print('URL não valida')
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

# def banana():
#     print("Fruta")

# x = 'banana'
# locals()[x]()

# ano = 20
# string = 'batata_{YYYY},2'
# print(string.format(YYYY=ano))
# print(re.findall('\{(.*?)\}',string))
# print(re.split(',', string))
# date = datetime.now()
# print(date + relativedelta(years=-1))

# x = [0,1,2]
# y = (a for a in x)
# for i in y:
#     print(i)