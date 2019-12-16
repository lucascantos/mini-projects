
def send_message(event, context=None):
    new_bot = telegram_bot()
    new_bot.send_message(message, client)

def clients_update(event, context=None):
    new_bot = telegram_bot(name)
    new_bot.clients_update()

import json
import logging
import os
from requests import post

# Helper function to prettify the message if it's in JSON  
def process_message(self, input):
    try:
        # Loading JSON into a string
        raw_json = json.loads(input)
        # Outputting as JSON with indents
        output = json.dumps(raw_json, indent=4)
    except:
        output = input
    return output



    
if __name__ == "__main__":
    event = {
        'message': "Oie. Msg vinda da api",
        'client': 'lucas',
        'command': 'getUpdates'
    }
    lambda_handler(event)