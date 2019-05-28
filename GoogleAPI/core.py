from GoogleSlides import GoogleSlide

def routine():
    
    # Caminho pros arquivos de autencticação     
    client_path = 'GoogleAPI/credentials/client_secret.json'
    service_path = './credentials/service_key.json'
    template_id = '1k2NX5dV6KPoyMq89phXFQ_QoOyhti4Sc9Yw6oDX97Z4'

    logo = {'file': 'logo.jpg', 'placeholder': '{{LOGO}}'}
    title = {'newTxt': '>Titulo', 'placeholder': '{{TITLE}}'}

    # Cria Conexão  com o Google e copia um template
    meuslide = GoogleSlide(client_path, template_id)
    meuslide.client_credenciais()

    meuslide.clone_presentation()

    # Monta a ordem dos objetos a serem substituidos a partir de um template
    meuslide.new_image(logo['file'], logo['placeholder'])
    meuslide.new_text(title['newTxt'], title['placeholder'])
    # pprint(meuslide.reqs)
    # Substitui os items
    meuslide.push_change()


def teste():
    # Caminho pros arquivos de autencticação     
    client_path = 'GoogleAPI/credentials/client_secret.json'
    service_path = './credentials/service_key.json'
    template_id = '1k2NX5dV6KPoyMq89phXFQ_QoOyhti4Sc9Yw6oDX97Z4'

    logo = {'file': 'logo.jpg', 'placeholder': '{{LOGO}}'}
    title = {'newTxt': '>Titulo', 'placeholder': '{{TITLE}}'}

    # Cria Conexão  com o Google e copia um template
    meuslide = GoogleSlide(client_path, template_id)
    meuslide.client_credenciais()
    meuslide.create_presentation()

    meuslide.add_slide('Batatinha')
    meuslide.push_change()

    '''  for k in meuslide.template_file['slides']: print(k['objectId'])
    for j  in meuslide.slide_list: print(j)'''

teste()