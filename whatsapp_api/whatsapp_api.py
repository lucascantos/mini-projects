import requests
import json

url = 'https://foo.chat-api.com/messages?lastMessageNumber=20:'
response = requests.get(url).content
messages = json.loads(response)['messages']
print(messages)

# for single_message in messages:
#     sampler = ['sender', 'chatId', 'body']
#     sample = [single_message[var] for var in sampler]
#     print(sample)

