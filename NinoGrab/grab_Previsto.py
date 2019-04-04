from grab_Object import NinoDataframe as ndf
import myconstants as const

def nome_arquivo(atributo):
    arquivo = '{}{}{}{file_atribute}{}{}_{}{}.csv'.format(const.anoA, const.mesA, const.diaA, const.ano, const.mes, const.anoD, const.mesD, file_atribute=atributo)
    return arquivo
# ----------------------------------------------------
# --------------------------Mensal--------------------
def grab_mensal():

    # --- Previsão ---
    monthly = ['http://dd.weather.gc.ca/ensemble/cansips/csv/indices/forecast/monthly/', '00_indices_month_', './ninos_data/mensal.csv']
    arquivo1 = nome_arquivo(monthly[1])
    caminho_mensal = monthly[0] + arquivo1
    columns_mensal = {'NINO1+2': 'ANOM12', 'NINO3': 'ANOM3', 'NINO4': 'ANOM4', 'NINO3.4': 'ANOM34'}

    df_previsto = ndf(caminho_mensal)
    x = df_previsto.download_database()
    if x:
        print('Arquvio Mensal Baixado com sucesso!')
    ndf.save_file(df_previsto.df_raw, arquivo1)
    df_previsto.cria_dataframe(columns_mensal, transpose=True)
    df_previsto.cria_index(const.ano + const.mes, const.anoD + const.mesD)
    return df_previsto
    #merged = pd.concat([df_observado.df,df_previsto.df], sort=True)
    #ndf.save_file(merged, 'mensal.csv')

# ----------------------------------------------------
# --------------------------Season--------------------

def grab_sasonal():
    seasonal = ['http://dd.weather.gc.ca/ensemble/cansips/csv/indices/forecast/seasonal/', '00_indices_season_', './ninos_data/seasonal.csv']
    arquivo2 = nome_arquivo(seasonal[1])
    caminho_season = seasonal[0] + arquivo2

    columns_season = {'NINO12': 'ANOM12', 'NINO3': 'ANOM3', 'NINO4': 'ANOM4', 'NINO3.4': 'ANOM34'}

    df_sasonal = ndf(caminho_season)
    x = df_sasonal.download_database()
    if x:
        print('Arquvio Sasonal Baixado com sucesso!')
    df_sasonal.save_file(df_sasonal.df_raw, arquivo2)
    df_sasonal.cria_dataframe(columns_season, transpose=True)
    df_sasonal.df['meses'] = df_sasonal.df.index

    df_sasonal.cria_index(const.ano1 + const.mes1, const.ano9 + const.mes9)

    return df_sasonal


    #merged_sasonal = pd.concat([df_observado.df_season, df_sasonal.df], sort=True)
    #ndf.save_file(merged_sasonal, 'sasonal.csv')