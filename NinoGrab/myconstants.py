# -Pega datas pra puxar arquivo do site. Data do mes passado, Hoje e data daqui a 12 meses
import pandas as pd
from pandas.tseries.offsets import MonthEnd

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

mes_quevem = (pd.to_datetime('today') + pd.DateOffset(months=1)) + MonthEnd(1)
mes1 = str(mes_quevem.strftime('%m'))
dia1 = str(mes_quevem.strftime('%d'))
ano1 = str(mes_quevem.year)

meses9 = (mes_quevem + pd.DateOffset(months=8)) + MonthEnd(1)
mes9 = str(meses9.strftime('%m'))
dia9 = str(meses9.strftime('%d'))
ano9 = str(meses9.year)
