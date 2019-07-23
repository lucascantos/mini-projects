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
class DownloadURL(object):
    def __init__(self, image_name, param=''):
        '''
        Classe que faz o download de uma imagem baseado no nome de uma variavel
        image_name: nome da variavel de referencia
        param: parametro extra opcional. (nome de cidade ou numero do mapa) (por hora, admite-se que só há 1 parametro extra)
        '''
        self.image_name = image_name
        self.database = 'database_link_or_url'
        self.today_date = datetime.utcnow()
        self.param = param
    
    def grab_url(self):
        '''
        Busca dentro do banco de dados a linha que contem os dados.
        '''
        data_row = self.database.loc[self.database['name'] == self.image_name]
        self.url = data_row.iloc[0]['file_url']
        timedelta = re.split(",", data_row.iloc[0]['timedelta'])
        self.time = [self.change_time(delta) for delta in timedelta]

        
        # single_image =  (index, data for index, data in self.database.iterrows())
        # for i in single_image:
            
        #     print(i)
        #     if i['name'] == self.image_name:
        #         '''
        #         Salva a url e monta uma lista com as datas que vão ser alteradas no link
        #         '''
        #         self.single_image = single_image
        #         self.url = single_image['file_url']
        #         timedelta = re.split(",", single_image['timedelta'])
        #         self.time = [self.change_time(delta) for delta in timedelta]
        #         break

    def split_param(self):
        '''
        Busca dentro da string URL por parametro entre {}.
        conta quantas vezes a variavel ja foi chamada e chama a data correspondente
        '''
        reference_list = []
        param_list = re.findall('\{(.*?)\}', self.url)
        for param in param_list:
            i = reference_list.count(param)
            if re.search('%', param):
                print(param)
                if param == '%H':
                     replacement = self.hour_default()
                     print(replacement)
                else:
                    replacement = self.time[i].strftime(param)               
            else:
                replacement = self.param
            
            self.url = self.url.replace('{'+param+'}', replacement)
            reference_list.append(param)

    def hour_default(self):
        if self.today_date.hour >= 12:
            return '12'
        else:
            return '00'

    def change_time(self, full_delta):
        '''
        função que converte o timedelt em data
        '''
        delta = int(full_delta[-2:])
        period = full_delta[:-2]
        keydelta = {period: delta}
        print(relativedelta(**keydelta))
        return self.today_date + relativedelta(**keydelta)
    

    def pdf_slicer(self):
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






