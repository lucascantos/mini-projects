from src.helpers.db import clients_connected
from src.helpers.message import send, response

def connection(event=None, context=None):
    event_context = event['requestContext']
    if event_context['eventType'] == 'CONNECT':
        clients_connected(event_context['connectionId'], 'add')
        return response['success']
    elif event_context['eventType'] == 'DISCONNECT':
        clients_connected(event_context['connectionId'], 'remove')
        return response['success']
    

def default(event=None, context=None):
    return response['default']
 

def send_msg (event=None, context=None):
    '''
    Pegar todos os IDs e retorn array
    '''
    print(event['requestContext'])
    client_list=event['requestContext']['connectionId']
    send(event, client_list)

    return response['success']

