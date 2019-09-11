import json 

def yeet(event, context):
    body = {
        "message": "Yeet",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
