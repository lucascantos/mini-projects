from GoogleSlides import GoogleSlide
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
    meuslide.push_change()

@timeit
def slide_by_slide():
    # Caminho pros arquivos de autencticação     
    client_path = 'GoogleAPI/credentials/client_secret.json'
    service_path = './credentials/service_key.json'
    template_id = '1k2NX5dV6KPoyMq89phXFQ_QoOyhti4Sc9Yw6oDX97Z4'

    logo = {'file': 'logo.jpg', 'placeholder': '{{LOGO}}'}
    title = {'newTxt': 'Meu Titulo', 'placeholder': '{{TITLE}}'}
    
    # Cria Conexão  com o Google e copia um template
    meuslide = GoogleSlide(client_path, template_id, )
    meuslide.client_credenciais()
    meuslide.create_presentation('Teste02')

    meuslide.add_slide('cenourinha') 
    meuslide.push_change()
    meuslide.add_image(logo['file'], logo['placeholder'])
    meuslide.add_text(title['newTxt'], title['placeholder'])
    meuslide.push_change()

    '''  for k in meuslide.template_file['slides']: print(k['objectId'])
    for j  in meuslide.slide_list: print(j)'''

slide_by_slide()