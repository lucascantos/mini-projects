import urllib.request
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
  

# Pega variaveis do link 
class imagem(object):
    def __init__(self, image_name, param=''):
        '''
        Classe que faz o download de uma imagem baseado no nome de uma variavel
        image_name: nome da variavel de referencia
        param: parametro extra opcional. (nome de cidade ou numero do mapa) (por hora, admite-se que só há 1 parametro extra)
        '''
        self.image_name = image_name
        self.database = 'database_link_or_url'
        self.today_date = datetime.utcnow
        self.param = param
    
    def grab_url(self):
        '''
        Busca dentro do banco de dados a linha que contem os dados.
        '''

        single_image =  (data for data in self.database)
        for i in single_image:
             if single_image['name'] == self.image_name:
                '''
                Salva a url e monta uma lista com as datas que vão ser alteradas no link
                '''
                self.single_image = single_image
                self.url = single_image['file_url']
                timedelta = re.split(",", single_image['timedelta'])
                self.time = [self.change_time(delta) for delta in timedelta]
                yield

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
                self.url = self.url.replace(param, self.time[i].strftime(param))
            else:
                self.url.replace(param, self.param)
            reference_list.append(param)

    def change_time(self, full_delta):
        '''
        função que converte o timedelt em data
        '''
        delta = int(full_delta[:2])
        period = full_delta[-1]
        keydelta = {period: delta}
        yield self.today_date + relativedelta(keydelta)

        



'''
    def text_split(self, file_url):
        # Pega o nome de dominio
        self.subdomain_list = file_url.split('/')
        for self.company in self.function_list():
            if re.search(self.company, self.subdomain_list[2]):            
                locals()[self.company]()                

    def function_list(self):
        l = []
        for key, value in locals().items():
            if callable(value) and value.__module__ == __name__:
                l.append(key)
        return l   
'''


def banana():
    print("Fruta")

x = 'banana'
locals()[x]()

ano = 20
string = 'batata_{YYYY},2'
print(string.format(YYYY=ano))
print(re.findall('\{(.*?)\}',string))
print(re.split(',', string))
date = datetime.now()
print(date + relativedelta(years=-1))

x = [0,1,2]
y = (a for a in x)
for i in y:
    print(i)






