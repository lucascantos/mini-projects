import json
import boto3
import base64
from src.helpers.db import clients_connected
from src.helpers.message import send, success_response

def connection(event=None, context=None):
    event_context = event['requestContext']
    if event_context['eventType'] == 'CONNECT':
        clients_connected(event_context['connectionId'], 'add')
        return success_response
    elif event_context['eventType'] == 'DISCONNECT':
        clients_connected(event_context['connectionId'], 'remove')
        return success_response
    

def default(event=None, context=None):
    return {
        'statusCode': 200,
        'body': 'Default route called!'
    }
 

def send_msg (event=None, context=None):
    '''
    Pegar todos os IDs e retorn array
    '''
    print(event['requestContext'])
    client_list=event['requestContext']['connectionId']
    # Enviar para cada um dos ids
    send(event, client_list)

    return success_response

