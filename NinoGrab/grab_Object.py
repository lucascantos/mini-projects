import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd

class NinoDataframe(object):
    def __init__(self, url):
        self.url = url

    def download_database(self,*,previsto=True):
        try:
            if previsto:
                self.df_raw = pd.read_csv(self.url, index_col=0)
            else:
                self.df_raw = pd.read_csv(self.url, delim_whitespace=True, header=0)
            return True
        except:
            print('Arquivo nao encontrado: {}'.format(self.url))
            print('Acesse o link pra testar')
            return False

    @staticmethod
    def save_file(df, filename='output.csv'):
        df.to_csv('./ninos_data/{}'.format(filename))

    def cria_dataframe(self, column_names,*,transpose=False):
        if transpose:
            self.df = self.df_raw.T
        else:
            self.df = self.df_raw
        self.df.columns = map(str.upper, self.df.columns)
        self.df.rename(columns=column_names, inplace=True)

    def cria_index(self, inicio, fim,*, df_indexed=None):
        self.lista_data = pd.date_range(start=inicio + '01', end=fim + '01', freq='MS')
        if df_indexed is None:
            df_indexed = self.df
        else:
            #self.lista_data = self.lista_data[1:]
            self.season_labels()
        df_indexed.index = (pd.to_datetime(self.lista_data))
        df_indexed.dropna(inplace=True)


    def media_sasonal(self, labels):
        self.df_season = pd.DataFrame()
        for i in range(0, 4, 1):
            anom = labels['Anoms'][i]

            # --Faz media entre tres dados para cada mes, adiciona 2 vazios e agrega
            df_mean = []
            for i in range(0, len(self.df_raw), 1):
                try:
                    media = self.df_raw[anom][i - 1: i + 2]
                    if len(media)==3:
                        df_mean.append(media.mean())
                    else:
                        df_mean.append(np.nan)
                except:
                    df_mean.append(np.nan)
            # --Armazena essa media em um novo Dataframe
            self.df_season[anom] = df_mean
        print(len(df_mean))
    def season_labels(self):
        # --Converte a lista em Dataframe, adiciona index, e uma coluna com o label trimestral

        season_label = {1: 'DJF',
                        2: 'JFM',
                        3: 'FMA',
                        4: 'MAM',
                        5: 'AMJ',
                        6: 'MJJ',
                        7: 'JJA',
                        8: 'JAS',
                        9: 'ASO',
                        10: 'SON',
                        11: 'OND',
                        12: 'NDJ'}
        lista_meses = self.lista_data.month
        self.df_season['meses'] = lista_meses
        self.df_season['meses'] = self.df_season['meses'].apply(lambda x: season_label[x])
