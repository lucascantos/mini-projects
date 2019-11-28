
import json
import boto3
from src.helpers.db import clients_connected

def send (event, client_list):
    event_context = event['requestContext']
    sender = event_context['connectionId']
    if event_context['routeKey']=='$default':
        message = f"{sender}: {event['body']}"
    else:
        body = json.loads(event['body'])
        message = f"{sender}: {body['data']}"
    endpoint = f"https://{event_context['domainName']}/{event_context['stage']}/"

    session = boto3.session.Session()
    client = session.client(
        service_name='apigatewaymanagementapi',
        endpoint_url = endpoint
    )
    if isinstance(client_list, str):
        client_list = [client_list]
    
    for client_id in client_list:
        if client_id != sender:
            try:
                client.post_to_connection(
                    Data=message, 
                    ConnectionId=client_id
                    )
            except:
                print(f'Invalid client_id! Disconeccting: {client_id}')
                clients_connected(client_id, 'REMOVE')
                

response = {
    'success': {
        'statusCode': 200,
        'body': 'Good!'
    },
    'failure': {
        'statusCode': 500,
        'body': 'Something failed!'
    },
    'default': {
        'statusCode': 200,
        'body': 'Default route called!'
    },
}