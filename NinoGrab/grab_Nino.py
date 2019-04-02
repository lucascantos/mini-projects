# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

from pandas.tseries.offsets import MonthEnd

grafico = {
    'Ninos': ['Nino1+2', 'Nino3', 'Nino4', 'Nino3.4'],
    'Anoms': ['ANOM12', 'ANOM3', 'ANOM4', 'ANOM34']
}

# ----------------------------------------------------
# --------------------------Mensal--------------------

# -Pega datas pra puxar arquivo do site. Data do mes passado, Hoje e data daqui a 12 meses

hoje = (pd.to_datetime('today'))
mes = str(hoje.strftime('%m'))
dia = str(hoje.strftime('%d'))
ano = str(hoje.year)

mes_passado = (pd.to_datetime('today') - pd.DateOffset(months=1)) + MonthEnd(1)
print('Usando a data de hoje: {}'.format(mes_passado))
mesA = str(mes_passado.strftime('%m'))
diaA = str(mes_passado.strftime('%d'))
anoA = str(mes_passado.year)
# _ano = str(2019)

Depois = mes_passado + pd.DateOffset(months=12)
diaD = str(Depois.strftime('%d'))
mesD = str(Depois.strftime('%m'))
anoD = str(Depois.year)
# anoD = str(2019)

# -Baixa arquivo de Previsao (por enquanto monthly)
monthly = ['http://dd.weather.gc.ca/ensemble/cansips/csv/indices/forecast/monthly/', '00_indices_month_']
try:
    arquivo = anoA + mesA + diaA + monthly[1] + ano + mes + '_' + anoD + mesD + '.csv'
    df = pd.read_csv(monthly[0] + arquivo, index_col=0)
    print(arquivo)

except:
    print('Arquivo nao encontrado. ' + arquivo)
    print('Acesse o link pra testar')
    print(monthly[0])

# -Salva num arquivo o dado bruto
df.to_csv('./ninos_data/' + arquivo, sep='\t')

df.rename(columns={'NINO1+2': 'ANOM12', 'NINO3': 'ANOM3', 'NINO4': 'ANOM4', 'NINO3.4': 'ANOM34'}, inplace=True)

# -Transpoem o Dataframe e renomeia as colunas pra somar aos observados

df_T = df.T
df_T.columns = map(str.upper, df_T.columns)
df_T.rename(columns={'NINO1+2': 'ANOM12', 'NINO3': 'ANOM3', 'NINO4': 'ANOM4', 'NINO3.4': 'ANOM34'}, inplace=True)

# -Baixa arquivo de Observação
obs = 'ftp://ftp.cpc.ncep.noaa.gov/wd52dg/data/indices/sstoi.indices'
df_obs = pd.read_csv(obs, delim_whitespace=True, header=0)
df_obs.rename(columns={'ANOM': 'ANOM12', 'ANOM.1': 'ANOM3', 'ANOM.2': 'ANOM4', 'ANOM.3': 'ANOM34'}, inplace=True)

# -Gera um novo dataframe somando observado e previsto
inicio = str(df_obs.YR[0]) + pd.to_datetime(df_obs.MON[0]).strftime('%m')
fim = anoD + mesD
lista_data = pd.date_range(start=inicio + '01', end=fim + '01', freq='MS')
obs_prev = df_obs.merge(df_T, how='outer')
obs_prev.index = (pd.to_datetime(lista_data))
obs_prev.to_csv('./ninos_data/mensal.csv')

# ----------------------------------------------------
# --------------------------Season--------------------
# Ta no mesmo script pq tem coisas como datas sendo reutilizadas. Mas so isso msm

mes_quevem = (pd.to_datetime('today') + pd.DateOffset(months=1)) + MonthEnd(1)
mes1 = str(mes_quevem.strftime('%m'))
dia1 = str(mes_quevem.strftime('%d'))
ano1 = str(mes_quevem.year)

meses10 = (mes_quevem + pd.DateOffset(months=9)) + MonthEnd(1)
print(meses10)
mes9 = str(meses10.strftime('%m'))
dia9 = str(meses10.strftime('%d'))
ano9 = str(meses10.year)

seasonal = ['http://dd.weather.gc.ca/ensemble/cansips/csv/indices/forecast/seasonal/', '00_indices_season_']

try:
    arquivo2 = anoA + mesA + diaA + seasonal[1] + ano + mes + '_' + anoD + mesD + '.csv'
    print(arquivo2)
    df = pd.read_csv(seasonal[0] + arquivo2, index_col=0)
except:
    print('Arquivo nao encontrado. ' + arquivo2)
    print('Acesse o link pra testar')
    print(seasonal[0])

# -Salva num arquivo o dado bruto
df.to_csv('./ninos_data/' + arquivo, sep='\t')

# -Transpoem o Dataframe e renomeia as colunas pra somar aos observados
df_T = df.T
df_T.columns = map(str.upper, df_T.columns)
df_T.rename(columns={'NINO12': 'ANOM12', 'NINO3': 'ANOM3', 'NINO4': 'ANOM4', 'NINO3.4': 'ANOM34'}, inplace=True)
season_label = {1: 'DJF', 2: 'JFM', 3: 'FMA', 4: 'MAM', 5: 'AMJ', 6: 'MJJ', 7: 'JJA', 8: 'JAS', 9: 'ASO', 10: 'SON',
                11: 'OND', 12: 'NDJ'}

# -Preparando Index, Mas nao deu certo entao dei um migueh ali na frente
inicio2 = str(df_obs.YR[0]) + pd.to_datetime(df_obs.MON[0]).strftime('%m')
fim2 = ano9 + mes9
lista_data2 = pd.date_range(start=inicio2 + '01', end=fim2 + '01', freq='MS')
lista_meses = lista_data2.month
df_final = pd.DataFrame()
print(inicio2, fim2)
for i in range(0, 4, 1):
    nino = grafico['Ninos'][i]
    anom = grafico['Anoms'][i]

    # --Faz media entre tres dados para cada mes, adiciona 2 vazios e agrega
    df_obs_mean = []
    for i in range(1, len(df_obs) - 1, 1):
        media = df_obs[anom][i - 1: i + 2]
        df_obs_mean.append(media.mean())
    df_obs_mean.append(np.nan)
    df_obs_mean.append(np.nan)
    for i in df_T[anom][:]:
        # print (i)
        df_obs_mean.append(i)
    # --Armazena essa media em um novo Dataframe
    df_final[anom] = df_obs_mean

    # --Converte a lista em Dataframe, adiciona index, e uma coluna com o label trimestral
    df_obs_mean = pd.DataFrame({anom: df_obs_mean})
    df_obs_mean.index = lista_data2[1:]
    df_obs_mean['meses'] = lista_meses[1:]
    df_obs_mean['meses'] = df_obs_mean['meses'].apply(lambda x: season_label[x])
    df_obs_mean = df_obs_mean.dropna()
    df_T = df_T.drop(columns=anom)

# print (df_T)
df_final.index = lista_data2[1:]
df_final['meses'] = df_obs_mean['meses']
df_final = df_final.dropna()
df_final.to_csv('./ninos_data/sasonal.csv')

