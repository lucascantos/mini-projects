import requests
from bs4 import BeautifulSoup
import pandas as pd

'''
Fontes: Somar, Climatempo, Terra, Uol, Google, G1, R7, 
Reddit: 
Twitter: defesacivilsp
'''

class GoogleSearchScrapper(object):
    def __init__(self, keys,*, date_ini, date_end,num=50):
        self.keys = keys
        self.date_ini = date_ini
        self.date_end = date_end
        self.num = num

    def google_search_url(self):
        base_google = 'https://www.google.com.br/search?'
        keywords = '+'.join(google_query['keyword'])
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        }

        parameters ={
            'tbs': 'cdr:1,cd_min:{ini},cd_max:{end}'.format(ini=self.date_ini, end=self.date_end),
            'num': '{num}'.format(num=self.num),
            'q': '{keywords}'.format(keywords=keywords),
            'tbm': 'nws'
        }


        self.search_url = '{}q={keywords}&tbm=nws&tbs=cdr:1,cd_min:{ini},cd_max:{end}&num={num}'.format(base_google, keywords=keywords, ini=self.date_ini, end=self.date_end,num=50)
        self.content = requests.get(base_google, params=parameters, headers=headers).content

    def google_search_parser(self):
        self.soup = BeautifulSoup(self.content, 'html.parser')
        weblinks = self.soup.findAll('div', class_='g')
        google_search_result = []

        for link in weblinks:
            header = link.findAll('a', class_='l')[0].text
            url = link.findAll('a', class_='l')[0]['href']
            source_date = link.findAll('div', class_='slp')
            for split in source_date:
                news_source = split.findAll('span')[0].text
                news_date = split.findAll('span')[2].text

            new_line = {'Header': header, 'url': url, 'Date': news_date, 'Source': news_source}
            line_df = pd.DataFrame([new_line], columns=new_line.keys())
            google_search_result.append(line_df)

        google_search_result = pd.concat(google_search_result, axis=0, ignore_index=True)
        self.output = google_search_result

    def print(self):
        print(self.soup.prettify())


keyword_weather = ['chuva']
keyword_place = ['campinas']

google_query = {
    'keyword': ['chuva', 'granizo', 'campinas'],
    'tye': 'news',
    'num': '50',
    'date': ['12/30/2016', '12/31/2016']
}

'''
https://github.com/NikolaiT/GoogleScraper/blob/master/GoogleScraper/search_engine_parameters.py
q : keyword
tbm : Special search. tbm=nws (GoogleNews)
tbs : Time range of search. tbs=cdr:1,cd_min:12/30/2015,cd_max:MM/DD/AAAA
df['DOB1'] = df['DOB'].dt.strftime('%m/%d/%Y'
'''

x = GoogleSearchScrapper(google_query['keyword'], date_ini=google_query['date'][0], date_end=google_query['date'][1])
x.google_search_url()
print(x.search_url)
x.google_search_parser()
print(x.output['Header'])
