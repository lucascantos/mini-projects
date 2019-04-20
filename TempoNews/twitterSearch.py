access_token = '182079485-3tw5jmfyBS0AyKPZoXBGj6bXPNJV6vM7EKF9EVM1'
access_token_secret = 'RokhIaTD7ybHB8Zki2dODThawzBEgtEBZPVXYasutGSFN'
client_key = 'wgUcW2uX4Ah70kUiqke7tHwSf'
client_secret = '5di38wMNbkxH2K70Lc7CTjXVjnmw117aSfZOqHv5xCasHNdDxB'

import json
import base64
import requests


key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

# Check status code okay
#print(auth_resp.status_code)

# Keys in data response are token_type (bearer) and access_token (your access token)
#print(auth_resp.json().keys())

access_token = auth_resp.json()['access_token']

search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)    
}

contas = ['defesacivilsp']
keywords = ['campinas', 'capital', 'campos']

search_params = {
    'q': 'campinas OR capital from:defesacivilsp',
    'count': '5',
}

statuses_params = {
    'screen_name': 'defesacivilsp',
    'count': 150,
}

search_url = '{}1.1/search/tweets.json'.format(base_url)
statuses_url = '{}1.1/statuses/user_timeline.json'.format(base_url)

#search_resp = requests.get(search_url, headers=search_headers, params=search_params) #https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
statuses_resp = requests.get(statuses_url, headers=search_headers, params=statuses_params) #https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html


tweet_data = statuses_resp.json()

print(len(tweet_data))

