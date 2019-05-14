import gspread
from apiclient import discovery
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

# Achar o Scope da API

img_file = ''
template_slide = ''

scope = ['https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/presentations']


'''
credentials = ServiceAccountCredentials.\
    from_json_keyfile_name('service_credentials.json', scope)

client = gspread.authorize(credentials)

sheet = client.open('Redecs e Mar').sheet1
data = sheet.get_all_records()
data = sheet.row_values(3)

sheet.update_cell(1, 4, 'AAAA')

new_row = ['AAA', 'BBB']
index = 1
sheet.insert_row(new_row, index)

print(data)
'''