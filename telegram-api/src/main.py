import json
import logging
from requests import post


# Initializing a logger and setting it to INFO
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

class telegram_bot(object):
    def __init__(self, name='lucas_cantos_bot'):
        self.RETRY = True
        self.name = name
        try:
            self.settings = bot_data[name]
            self.clients = self.settings['clients']
        except KeyError:
            raise KeyError("Bot name not found!")

    def update_clients(self):
        response = self._post_api('getUpdates')
        for post in json.loads(response.content)['result']:
            print(post)
            chat = post['message']['chat']
            if not chat['id'] in self.clients and "title" in chat:
                self.clients[chat['title']] = chat['id']

        bot_data[self.name] = self.settings
        # s3.upload('bots_settings', bot_data) 


    def send_message(self, message, client):
        try:
            CHAT_ID = self.clients[client]
        except KeyError:
            if self.RETRY:
                self.RETRY=False
                print('Retrying...')
                self.update_clients()
            else:
                self.RETRY=True
                raise KeyError("Client name not found!")
            

        payload = {"text": self.process_message(message).encode("utf8"), "chat_id": CHAT_ID}
        self._post_api('sendMessage', payload)

    def _post_api(self, command, payload={}):
        final_url = f"https://api.telegram.org/bot{self.settings['token']}/{command}"
        return post(final_url, payload)

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

    def open_json(path):
        with open(path, 'r') as f:
            return json.load(f)
            
    tokens_json = 'credentials/telegram.json'
    bot_data = open_json(tokens_json)
    new_bot = telegram_bot()
    new_bot.update_clients()
    new_bot.send_message('Yeet', 'lucas')
else:
    bot_data = s3.get_file('bots_settings')