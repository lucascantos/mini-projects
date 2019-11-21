import json
import boto3

success_response = {
        'statusCode': 200,
        'body': 'Good!'
    }

def connection(event=None, context=None):
    print(event)
    event_context = event['requestContext']
    print(event_context)
    print(context)
    if event_context['eventType'] == 'CONNECT':
        clients_connected(event_context.connectionId, 'add')
        return success_response
    elif event_context['eventType'] == 'DISCONNECT':
        clients_connected(event_context.connectionId, 'remove')
        return success_response
        pass

def default(event=None, context=None):
    pass 

def send_msg (event=None, context=None):
    '''
    Pegar todos os IDs e retorn array
    '''
    client_list=[]
    # Enviar para cada um dos ids
    send(event, client_list)

    return success_response

def send (event, client_id):
    event_context = event['requestContext']
    body = json.loads(event['body'])
    data = body['data']

    endpoint = f"{event_context['domainName']}/{event_context['stage']}/{client_id}"

    # session = boto3.session.Session()

    # client = session.client(
    #     service_name='apigatewaymanagementapi',
    #     endpoint_url='http://localhost:3001/'
    # )

    client = boto3.client('apigatewaymanagementapi')
    client.post_to_connection(
        Data=data, 
        ConnectionId=client_id
    )

def clients_connected (client_id, action):
    action = action.upper()
    if action == "ADD":
        pass
    elif action == 'REMOVE':
        pass
    else:
        print("action must be 'add' or 'remove' ")
