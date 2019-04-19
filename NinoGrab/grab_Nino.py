import grab_Observado as go
import grab_Previsto as gp
from grab_Object import NinoDataframe as ndf
import pandas as pd

observado = go.grab_observado()
mensal = gp.grab_mensal()
sasonal = gp.grab_sasonal()

merged1 = pd.concat([observado.df,mensal.df], sort=True)
ndf.save_file(merged1, 'mensal.csv')

merged2 = pd.concat([observado.df_season,sasonal.df], sort=True)
ndf.save_file(merged2, 'sasonal.csv')