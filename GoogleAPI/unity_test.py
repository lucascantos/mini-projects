from google_slides import GoogleSlide
from google_sheets import GoogleSheets
from google_credential import GoogleDrive
from image_grabber import DownloadURL
from time import time

def timeit (function):
    def wrapper(*args, **kwargs):
        antes = time()
        function(*args, **kwargs)
        depois = time()
        print ('Demorou {}segundos'.format(depois-antes))
    return wrapper

@timeit
def full_template():
    
    # Caminho pros arquivos de autencticação     
    client_path = 'GoogleAPI/credentials/client_secret.json'
    service_path = './credentials/service_key.json'
    template_id = '1k2NX5dV6KPoyMq89phXFQ_QoOyhti4Sc9Yw6oDX97Z4'

    logo = {'file': 'logo.jpg', 'placeholder': '{{LOGO}}'}
    title = {'newTxt': '>Titulo', 'placeholder': '{{TITLE}}'}

    # Cria Conexão  com o Google e copia um template
    meuslide = GoogleSlide(client_path, template_id)
    meuslide.client_credenciais()

    meuslide.clone_presentation('Teste01')

    # Monta a ordem dos objetos a serem substituidos a partir de um template
    meuslide.add_image(logo['file'], logo['placeholder'])
    meuslide.add_text(title['newTxt'], title['placeholder'])
    # pprint(meuslide.reqs)
    # Substitui os items

@timeit
def slide_by_slide():
    # Caminho pros arquivos de autencticação     
    client_path = 'GoogleAPI/credentials/client_secret.json'
    service_path = './credentials/service_key.json'
    template_id = '1k2NX5dV6KPoyMq89phXFQ_QoOyhti4Sc9Yw6oDX97Z4'

    logo = {'file': 'logo.jpg', 'placeholder': '{{LOGO}}'}
    title = {'newTxt': 'Meu Titulo', 'placeholder': '{{TITLE}}'}
    graph = {'url': 'https://i.kym-cdn.com/photos/images/original/000/124/933/1304376955947.png', 'placeholder': '{{TABLE2}}'}
    
    # Cria Conexão  com o Google e copia um template
    meuslide = GoogleSlide(client_path, template_id)
    meuslide.client_credenciais()
    meuslide.create_presentation('Teste02')

    meuslide.add_slide('cenourinha') 
    meuslide.push_change()

    meuslide.add_image(logo['file'], logo['placeholder'])
    meuslide.add_image(graph['url'], graph['placeholder'])
    meuslide.add_text(title['newTxt'], title['placeholder'])
    meuslide.push_change()

    '''  for k in meuslide.template_file['slides']: print(k['objectId'])
    for j  in meuslide.slide_list: print(j)'''

def build_template():
        # Caminho pros arquivos de autencticação     
    client_path = 'GoogleAPI/credentials/client_secret.json'
    service_path = './credentials/service_key.json'
    template_id = '1k2NX5dV6KPoyMq89phXFQ_QoOyhti4Sc9Yw6oDX97Z4'

    logo = {'file': 'logo.jpg', 'placeholder': '{{LOGO}}'}
    title = {'newTxt': 'Meu Titulo', 'placeholder': '{{TITLE}}'}
    
    # Cria Conexão  com o Google e copia um template
    meuslide = GoogleSlide(client_path, template_id)

    meuslide.client_credenciais()
    id = '1x1Qt7RBULCAVtJmad4Isct6ElwOWJRrLAWm2EWn7AxU'
    meuslide.template_builder(id)

def get_spreadsheet():
            # Caminho pros arquivos de autencticação     
    client_path = 'GoogleAPI/credentials/client_secret.json'
    service_path = './credentials/service_key.json'

    minhatablea = GoogleSheets(client_path)
    minhatablea.client_credenciais()
    minhatablea.grab_spreadsheet('Imagens')
    y = minhatablea.make_dataframe()

    minha_imagem = DownloadURL('prec_mensal')
    minha_imagem.database = y
    minha_imagem.grab_url()
    minha_imagem.split_param()
    print(minha_imagem.url)

def drive():
   
    import urllib
    import urllib3
    import requests

    client_path = 'GoogleAPI/credentials/client_secret.json'
    service_path = './credentials/service_key.json'
    target_image = 'https://i.kym-cdn.com/photos/images/original/000/124/933/1304376955947.png'
    local_image = 'GoogleAPI\imagem 1.png'

    drive = GoogleDrive(client_path)
    drive.client_credenciais()
    #x = drive.get_fileid('Imagens')


#slide_by_slide()
#full_template()
#build_template()
get_spreadsheet()
#drive()