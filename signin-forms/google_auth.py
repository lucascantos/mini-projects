
from apiclient import discovery
import httplib2
from oauth2client import client
from flask import Flask, request, Response

app = Flask(__name__)

# (Receive auth_code by HTTPS POST)
@app.after_request
def add_header(response):
    response.headers.add('Access-Control-Allow-Origin', '*')


    response.headers.add("Access-Control-Allow-Methods", "POST, GET")
    response.headers.add("Access-Control-Max-Age", "3600")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
    response.cache_control.max_age = 600
    return response

@app.route('/home', methods=['POST'])
def home():
    auth_code = request.args.get('data')
    auth(auth_code)
    return Response(auth_code)

def auth(auth_code):
    # If this request does not have `X-Requested-With` header, this could be a CSRF
    if not request.headers.get('X-Requested-With'):
        abort(403)

    # Set path to the Web application client_secret_*.json file you downloaded from the
    # Google API Console: https://console.developers.google.com/apis/credentials
    CLIENT_SECRET_FILE = 'credentials/client_web.json'

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['https://www.googleapis.com/auth/drive', 'profile', 'email'],
        auth_code)

    # Call Google API
    http_auth = credentials.authorize(httplib2.Http())
    print(http_auth)
    drive_service = discovery.build('drive', 'v3', http=http_auth)

    # Get profile info from ID token
    userid = credentials.id_token['sub']
    email = credentials.id_token['email']

    print(email)
    # file_list = drive_service.files().list(q='name=BandVale').execute()['files'][0]
    appfolder = drive_service.files().get(fileId='1iNLwHhp7gvnZWxgwRZjegKe5qO7b7B9zr7xf5KtZl9w').execute()
    print(appfolder)




if __name__ == '__main__':
    app.run(debug=True)
