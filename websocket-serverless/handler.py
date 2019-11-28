from src.helpers.db import clients_connected
from src.helpers.message import send, response
from src.helpers.s3 import s3_download

def connection(event=None, context=None):
    event_context = event['requestContext']
    if event_context['eventType'] == 'CONNECT':
        clients_connected(event_context['connectionId'], 'add')
        return response['success']
    elif event_context['eventType'] == 'DISCONNECT':
        clients_connected(event_context['connectionId'], 'remove')
        return response['success']
    

def default(event=None, context=None):
    # print(event)
    client_list = s3_download()['connected']
    send(event, client_list)
    return response['default']
 
def broadcast (event=None, context=None):
    '''
    Pegar todos os IDs e retorn array
    # {"action":"sendMessage", "data":"Hello World"}

    '''
    # client_list=event['requestContext']['connectionId']
    client_list = s3_download()['connected']
    send(event, client_list)

    return response['success']


