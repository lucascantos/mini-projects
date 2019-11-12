import requests
import json
from datetime import datetime

token_url = 'credentials/tokens.json'
with open(token_url) as f:
    tokens = json.load(f)

chat_token = tokens['chatapi']
url = 'https://eu5.chat-api.com/instance78956/'


read_url = f'{url}/messages?token={chat_token}'
send_url = f'{url}/sendMessage?token={chat_token}'

def ts_date(timestamp):
    time = datetime.fromtimestamp(timestamp)
    return time.strftime('%Y-%m-%d %H:%M')

def read_msg():        
    response = requests.get(read_url).content
    messages = json.loads(response)['messages']
    for single_message in messages:
        sampler = ['senderName', 'chatId']
        sample = [single_message[var] for var in sampler]
        print(sample, ts_date(single_message['time']))
        
read_msg()

def send_msg():
    data = {
        'phone': '5511970679442',
        'body': 'Hello Clarice'
    }
    headers = {
        'contentType': 'application/json',
        'type': 'POST'}
    requests.put(send_url, data=json.dumps(data), headers=headers)

    print('done')


