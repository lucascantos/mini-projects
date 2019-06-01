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

# Le arquivo
df = pd.read_csv('CEMADEN/SP_2019_3.csv', index_col=False, sep=';')

# Converte em Timeseries
df['datahora'] = pd.to_datetime(df['datahora'])
df = df.set_index('datahora')
df.drop(['datahora'], axis=1, inplace=True)

# Troca virgula por ponto e converte o valor de str pra float
df = df.replace({',':'.'}, regex=True).apply(pd.to_numeric,1)

cidade = 'Mauá'
# Pra cada Cidade
filtro_cidade = [df['municipio'] == upper(cidade)]
# Pra cada Periodo
df['2019-03-10 03:00:00':'2019-03-11 03:00:00']
# Pra cada estação
for df_estacao in df['codEstacao'].unique():
    pass

df[:][filtro_cidade]



'''Separar Data e Hora'''

