import pandas as pd
from datetime import datetime

cidades = [
    'São Bernardo do Campo',
    'São Caetano do Sul',
    'Santo André', 
    'Ribeirão Pires',
    'Mauá',
    'Diadema',
    'Rio Grande da Serra'
    'São Paulo',
    'Embu das Artes'
]

file = 'CEMADEN\SP_2019_3.csv'

class cemaden_data(object):
    def __init__(self, start_date, end_date, cities):
        '''      
        date: Tanto faz a ordem. O pandas tenta fazer dar certo. Ja converte pra UTC (+3h)
        cities: Lista de cidades
        '''
        self.start_date = pd.to_datetime(start_date, dayfirst=True)
        self.end_date = pd.to_datetime(end_date dayfirst=True)
        self.date_range = pd.date_range(self.start_date, self.end_date, freq='D')
        self.cities = cities


    def open_cemaden_csv(self, file)
        ''' file: Arquivo CSV com dados no formato do CEMADEN'''
        self.df = pd.read_csv(file, index_col=False, sep=';')
        self.df.resample()

    def make_timeseries(self)
        ''' Converte em Timeseries'''
        self.df['datahora'] = pd.to_datetime(df['datahora'])
        self.df = df.set_index('datahora')
        # df.drop(['datahora'], axis=1, inplace=True)
    def str2float(self):
        '''
        Transforma as colunas de lat, lon, valor em numeros
        '''
        # Troca virgula por ponto e converte o valor de str pra float
        self.df.replace({',':'.'}, regex=True, inplace=True)

        self.df['valorMedida'] = df['valorMedida'].apply(pd.to_numeric, 1, errors='ignore')        
        self.df['latitude'] = df['latitude'].apply(pd.to_numeric, 1, errors='ignore')        
        self.df['longitude'] = df['longitude'].apply(pd.to_numeric, 1, errors='ignore')
    
    def group_city_staion(self):
        # Agrupa por cidade e depois por Estacao
        grouped_df = df.groupby(['municipio', 'nomeEstacao'])
        # Agora agrupado, faz a soma diaria dos dados
        grouped_df = grouped_df.resample('D', loffset=pd.DateOffset(hours=3)).sum()

    def filters(self):        
        for city in self.cities:
            for date in self.date_range:
                yield grouped_df.loc[city, slice(None), date.strftime('%Y-%m-%d')]

    for city in self.cities:
        df['']

cidade = 'Mauá'
# Pra cada Cidade
filtro_cidade = [df['municipio'] == upper(cidade)]
# Pra cada Periodo
df['2019-03-10 03:00:00':'2019-03-11 03:00:00']
# Pra cada estação
for df_estacao in df['codEstacao'].unique():
    pass

df[:][filtro_cidade]
