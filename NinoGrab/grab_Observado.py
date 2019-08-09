import pandas as pd
from grab_Object import NinoDataframe
import myconstants as const

def grab_observado():

    # --- Observação Mensal ---
    caminho_observado = 'ftp://ftp.cpc.ncep.noaa.gov/wd52dg/data/indices/sstoi.indices'
    columns_observado = {'ANOM': 'ANOM12', 'ANOM.1': 'ANOM3', 'ANOM.2': 'ANOM4', 'ANOM.3': 'ANOM34'}

    df_observado = NinoDataframe(caminho_observado)
    df_observado.download_database(previsto=False)

    anos = df_observado.df_raw.YR
    meses = df_observado.df_raw.MON

    ini = str(anos[0]) + pd.to_datetime(meses[0]).strftime('%m')
    fim = str(anos.iloc[-1]) + str(meses.iloc[-1]).zfill(2)
    df_observado.cria_dataframe(columns_observado)
    df_observado.cria_index(ini, fim)

    # --- Observação Sasonal ---

    grafico = {
        'Ninos': ['Nino1+2', 'Nino3', 'Nino4', 'Nino3.4'],
        'Anoms': ['ANOM12', 'ANOM3', 'ANOM4', 'ANOM34']
    }
    df_observado.media_sasonal(grafico)
    # print(df_observado.df_raw.tail())
    df_observado.cria_index(ini, fim, df_indexed=df_observado.df_season)
    print(df_observado.df_season.tail())
    print('Dados observados atualizados.')
    return df_observado
