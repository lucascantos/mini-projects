import requests
from bs4 import BeautifulSoup
import pandas as pd

'''
Fontes: Somar, Climatempo, Terra, Uol, Google, G1, R7, 
Reddit: 
Twitter: defesacivilsp
'''

keyword_weather = ['chuva']
keyword_place = ['campinas']

google_query = {
    'keyword': ['chuva', 'granizo', 'alagado', 'campinas', '-previsão'],
    'tye': 'news',
    'num': '50',
    'date': ['12/30/2018', '12/31/2018']
}

'''
https://github.com/NikolaiT/GoogleScraper/blob/master/GoogleScraper/search_engine_parameters.py
q : keyword
tbm : Special search. tbm=nws (GoogleNews)
tbs : Time range of search. tbs=cdr:1,cd_min:12/30/2015,cd_max:MM/DD/AAAA
df['DOB1'] = df['DOB'].dt.strftime('%m/%d/%Y'
'''

base_google = 'https://www.google.com.br/search?'
keywords = '+'.join(google_query['keyword'])
search_url = '{}q={keywords}&tbm=nws&tbs=cdr:1,cd_min:{ini},cd_max:{end}&num={num}'.format(base_google, keywords=keywords, ini=google_query['date'][0], end=google_query['date'][1],num=google_query['num'])

r = requests.get(search_url).content
soup = BeautifulSoup(r, 'html.parser')

print(soup.prettify())
weblinks = soup.findAll('div', class_='g')

news_header = []
news_url = []
news_source = []
news_date = []

for link in weblinks:
    news_header[-1] = link.findAll('a')[0].text
    url = link.findAll('a')[0]['href'][7:]
    source_date = link.findAll('span', class_='f')[0].text
    news_source, news_date = source_date.split('-')


