
import json
import boto3

def send (event, client_id):
    event_context = event['requestContext']
    body = json.loads(event['body'])
    data = body['data']

    endpoint = f"https://{event_context['domainName']}/{event_context['stage']}/"

    # client = boto3.client('apigatewaymanagementapi')
    session = boto3.session.Session()
    client = session.client(
        service_name='apigatewaymanagementapi',
        endpoint_url = endpoint
    )

    client.post_to_connection(
        Data=data, 
        ConnectionId=client_id
    )


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