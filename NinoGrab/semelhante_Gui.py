import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import MonthEnd

# DADOS BASICOS PRA MEXER
# -------------------------------
porcentagem = 0.5  # O quao similar deve ser a comparacao entre a referencia e o ano anterior. 1 = 100%
streak = 4  # Quantos pontos sequenciais devem ter para ser considerado similar.
anos_atras = 40  # Ate quantos anos atras gostaria de fazer a comparacao.
# -------------------------------

# -Dados pra fazer loop
grafico = {
    'Ninos': ['Nino1+2', 'Nino3', 'Nino4', 'Nino3.4'],
    'Anoms': ['ANOM12', 'ANOM3', 'ANOM4', 'ANOM34'],
    'Color': ['b', 'r', 'k', 'g']
}
count = 0
maior = 0
# -Pega datas de hoje e data daqui a 12 meses
# -Data do mes passado (Primeiro dia da previsao)


# Abrir arquivo
arquivo = './ninos_data/mensal.csv'
df = pd.read_csv(arquivo, index_col=0)
# print(df.ANOM)

# selecionar data central
mes_passado = (pd.to_datetime('today') - pd.DateOffset(months=1)) + MonthEnd(1)
print('Usando a data de hoje:', mes_passado)
mes = str(mes_passado.strftime('%m'))
dia = str(mes_passado.strftime('%d'))
ano = str(mes_passado.year)


# selecionar data de fim (apenas ano. Mes pode pegar do central)
def grabDates(date):
    inicio = date - pd.DateOffset(months=6)
    final = date + pd.DateOffset(months=12)
    ano_ini = inicio.year
    ano_fim = final.year
    mes_ini = inicio.month
    mes_fim = final.month
    return ano_ini, ano_fim, mes_ini, mes_fim


# fazer subset do dataframe com os ultimos valores
ano_ini, ano_fim, mes_ini, mes_fim = grabDates(mes_passado)

data_ini = pd.to_datetime(str(ano_ini) + '-' + str(mes_ini))
data_fim = pd.to_datetime(str(ano_fim) + '-' + str(mes_fim))

subsetPrev = df[str(data_ini):str(data_fim)].reset_index(drop=True).dropna(axis='columns')
subsetPrev = subsetPrev.dropna(axis='columns')
subsetPrev.columns = ['ANOM12P', 'ANOM3P', 'ANOM4P', 'ANOM34P']

subset12 = df.ANOM12[str(data_ini):str(data_fim)]
subset34 = df.ANOM34[str(data_ini):str(data_fim)]
# salvar subset
fig, ax = plt.subplots(figsize=(10.80, 6.00), dpi=100)
ax.plot(pd.to_datetime(subset12.index[:]), subset12[:], linestyle='--',
        label=(str(data_ini.year) + '/' + str(data_fim.year)))

for j in range(1, anos_atras, 1):
    # fazer subset com data -1 ano
    data_ini = (pd.to_datetime(str(ano_ini) + '-' + str(mes_ini)) - pd.DateOffset(years=j))
    data_fim = (pd.to_datetime(str(ano_fim) + '-' + str(mes_fim)) - pd.DateOffset(years=j))

    subset = df[str(data_ini):str(data_fim)].reset_index(drop=True)  # Tentando deixar generico pra dinamico
    subset = pd.concat([subset, subsetPrev], axis=1, sort=False)
    subset = subset.dropna(axis='columns')

    subset12_compare = df.ANOM12[str(data_ini):str(data_fim)]
    subset34_compare = df.ANOM34[str(data_ini):str(data_fim)]

    subset12_ratio = subset12.reset_index(drop=True) / subset12_compare.reset_index(drop=True)
    subset12_34 = subset12_compare.reset_index(drop=True) - subset34_compare.reset_index(drop=True)
    print("Yeet", subset12[0], subset12_compare[0], subset34_compare[0])

    print(subset['ANOM12P'] / subset['ANOM12'])
    exit()
    quit()
    # comparar esse subset com subset-1

    # _COMPARE = Valor da anomalia do Nino.XX em anos anteriores ao de referencia
    # _RATIO = razao entre Nino.XX de referencia com deanos anteriores
    # 12_34 = Diferenca entre Nino1+2 com Nino3.4

    for i in range(len(subset12_ratio)):
        if porcentagem < subset12_ratio[i] < (1 - porcentagem) + 1:
            # if ((porcentagem  <subset12_ratio[i]<((1-porcentagem)+1)) and (subset12_compare[i] > 1 and subset34_compare[i] > 1) and (subset12_34[i] > 1)):
            # print (i)
            count += 1
            if count > maior:
                maior = count
        else:
            count = 0

    # print(maior)
    # se o streak for bom, salvar subset-1 e label
    if maior >= streak:
        print('Esse periodo e parecido com ' + str(data_ini.year) + '(' + str(j) + ' anos atras)')
        # plotar subsets usando o index do primeiro como eixo X
        ax.plot(pd.to_datetime(subset12.index[:]), subset12_compare[:],
                label=(str(data_ini.year) + '/' + str(data_fim.year)))

    maior = 0
    count = 0

ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
plt.legend(fontsize='small', loc='lower center', fancybox=True, shadow=True, ncol=4)
plt.title('Anom. Nino1+2 / Limiar(%): ' + str(porcentagem) + '/ Streak: ' + str(streak))
fig.savefig('./ninos_images/AAA.png')
plt.show()


