import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd

class Dataframe(object):
    def __init__(self, url):
        self.url = url

    def download_database(self,*,previsto=True):
        try:
            if previsto:
                self.df_raw = pd.read_csv(self.url, index_col=0)
            else:
                self.df_raw = pd.read_csv(self.url, delim_whitespace=True, header=0)

            #self.df_raw.to_csv('./ninos_data/' + arquivo, sep='\t')
            print('Sucesso!')
            #return df

        except:
            print('Arquivo nao encontrado: {}'.format(url))
            print('Acesse o link pra testar')
            #return False

    def cria_dataframe(self, column_names,*,transpose=False):
        if transpose:
            self.df = self.df_raw.T
        else:
            self.df = self.df_raw
        self.df.columns = map(str.upper, self.df.columns)
        self.df.rename(columns=column_names, inplace=True)

    def cria_index(self, inicio, fim):
        lista_data = pd.date_range(start=inicio + '01', end=fim + '01', freq='MS')
        self.df.index = (pd.to_datetime(lista_data))

# --------------------------Mensal--------------------
# -Pega datas pra puxar arquivo do site. Data do mes passado, Hoje e data daqui a 12 meses

hoje = (pd.to_datetime('today'))
mes = str(hoje.strftime('%m'))
dia = str(hoje.strftime('%d'))
ano = str(hoje.year)

mes_passado = (pd.to_datetime('today') - pd.DateOffset(months=1)) + MonthEnd(1)
mesA = str(mes_passado.strftime('%m'))
diaA = str(mes_passado.strftime('%d'))
anoA = str(mes_passado.year)

Depois = mes_passado + pd.DateOffset(months=12)
diaD = str(Depois.strftime('%d'))
mesD = str(Depois.strftime('%m'))
anoD = str(Depois.year)

# ----------------------------------------------------
# --------------------------Mensal--------------------

# --- Observação ---
caminho_observado = 'ftp://ftp.cpc.ncep.noaa.gov/wd52dg/data/indices/sstoi.indices'
columns_observado = {'ANOM': 'ANOM12', 'ANOM.1': 'ANOM3', 'ANOM.2': 'ANOM4', 'ANOM.3': 'ANOM34'}

df_observado = Dataframe(caminho_observado)
df_observado.download_database(previsto=False)

anos = df_observado.df_raw.YR
meses = df_observado.df_raw.MON
ini = str(anos[0]) + pd.to_datetime(meses[0]).strftime('%m')
fim = str(anos.iloc[-1]) + str(meses.iloc[-1]).zfill(2)
df_observado.cria_dataframe(columns_observado)
df_observado.cria_index(ini, fim)

# --- Previsão ---
monthly = ['http://dd.weather.gc.ca/ensemble/cansips/csv/indices/forecast/monthly/', '00_indices_month_']
arquivo = anoA + mesA + diaA + monthly[1] + ano + mes + '_' + anoD + mesD + '.csv'
caminho_mensal = monthly[0] + arquivo
columns_mensal = {'NINO1+2': 'ANOM12', 'NINO3': 'ANOM3', 'NINO4': 'ANOM4', 'NINO3.4': 'ANOM34'}
range = {'ini': ano + mes, 'fim': anoD + mesD}

df_previsto = Dataframe(caminho_mensal)
df_previsto.download_database()
df_previsto.cria_dataframe(columns_mensal, transpose=True)
df_previsto.cria_index(range['ini'], range['fim'])

merged = pd.concat([df_observado.df,df_previsto.df], sort=True)

# ----------------------------------------------------
# --------------------------Season--------------------
# Ta no mesmo script pq tem coisas como datas sendo reutilizadas. Mas so isso msm
mes_quevem = (pd.to_datetime('today') + pd.DateOffset(months=1)) + MonthEnd(1)
mes1 = str(mes_quevem.strftime('%m'))
dia1 = str(mes_quevem.strftime('%d'))
ano1 = str(mes_quevem.year)

meses10 = (mes_quevem + pd.DateOffset(months=9)) + MonthEnd(1)
mes9 = str(meses10.strftime('%m'))
dia9 = str(meses10.strftime('%d'))
ano9 = str(meses10.year)

seasonal = ['http://dd.weather.gc.ca/ensemble/cansips/csv/indices/forecast/seasonal/', '00_indices_season_']
arquivo2 = anoA + mesA + diaA + seasonal[1] + ano + mes + '_' + anoD + mesD + '.csv'
caminho_season = seasonal[0] + arquivo2

columns_season = {'NINO12': 'ANOM12', 'NINO3': 'ANOM3', 'NINO4': 'ANOM4', 'NINO3.4': 'ANOM34'}
season_label = {1: 'DJF', 2: 'JFM', 3: 'FMA', 4: 'MAM', 5: 'AMJ', 6: 'MJJ', 7: 'JJA', 8: 'JAS', 9: 'ASO', 10: 'SON', 11: 'OND', 12: 'NDJ'}

df_sasonal = Dataframe(caminho_season)
df_sasonal.download_database()
df_sasonal.cria_dataframe(columns_season, transpose=True)