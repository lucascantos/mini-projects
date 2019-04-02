# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.tseries.offsets import MonthEnd

grafico = {
    'Ninos': ['Nino1+2', 'Nino3', 'Nino4', 'Nino3.4'],
    'Anoms': ['ANOM12', 'ANOM3', 'ANOM4', 'ANOM34'],
    'Color': ['b', 'r', 'k', 'g']
}

# selecionar data central
Hoje = (pd.to_datetime('today'))
print('Usando a data de hoje:', Hoje)
mes = str(Hoje.strftime('%m'))
dia = str(Hoje.strftime('%d'))
ano = str(Hoje.year)

mes_passado = (Hoje - pd.DateOffset(months=1)) + MonthEnd(1)
print('Usando a data de hoje:', mes_passado)
mesA = str(mes_passado.strftime('%m'))
diaA = str(mes_passado.strftime('%d'))
anoA = str(mes_passado.year)

Depois = mes_passado + pd.DateOffset(months=12)
diaD = str(Depois.strftime('%d'))
mesD = str(Depois.strftime('%m'))
anoD = str(Depois.year)


# selecionar data de fim (apenas ano. Mes pode pegar do central)
def grabDates(date):
    inicio = date - pd.DateOffset(months=12)
    final = date + pd.DateOffset(months=12)
    ano_ini = inicio.year
    ano_fim = final.year
    mes_ini = inicio.month
    mes_fim = final.month
    return ano_ini, ano_fim, mes_ini, mes_fim


# fazer subset do dataframe com os ultimos valores
ano_ini, ano_fim, mes_ini, mes_fim = grabDates(Hoje)

data_ini = pd.to_datetime(str(ano_ini) + '-' + str(mes_ini))
data_fim = pd.to_datetime(str(ano_fim) + '-' + str(mes_fim))

# ----------------------------------------------------
# --------------------------Mensal--------------------

# Abrir arquivos
try:
    arquivo = './Nino/ninos_data/mensal.csv'
    df = pd.read_csv(arquivo, index_col=0)
except:
    arquivo = './ninos_data/mensal.csv'
    df = pd.read_csv(arquivo, index_col=0)

print('Graficos mensais')
for i in range(0, 4, 1):
    nino = grafico['Ninos'][i]
    anom = grafico['Anoms'][i]
    print(anom, nino)
    subset = df[[anom, 'PDO']][str(data_ini):str(data_fim)]
    # print (subset)
    if subset[anom].max() > 2:
        L = 4
    else:
        L = 2
    fig, ax = plt.subplots(figsize=(10.80, 6.00), dpi=100)

    # --Separa o plot em Observado e Previsto. Obs recebe ultima linha do Prev pra evitar o buraco no plot
    subPrev = subset.dropna()[anom]
    subObs = subset[subset.isnull().any(axis=1)][anom]
    subObs = subObs.append(subPrev.iloc[[0]], ignore_index=False)

    ax.plot(pd.to_datetime(subObs.index), subObs, 'b--')
    ax.plot(pd.to_datetime(subPrev.index), subPrev, 'b-')

    # --Perfumaria do grafico
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%y"))
    plt.title('Indice ' + str(nino) + ' Observado X Previsao')
    plt.ylim(-1 * L, L)
    plt.xticks(subset[anom].index, rotation=45)
    plt.grid(True)
    plt.ylabel('Anomalia de temp (C)')

    plt.axhspan(0.5, L, facecolor='r', alpha=0.4)
    plt.axhspan(-0.5, -1 * L, facecolor='b', alpha=0.4)
    fig.savefig('./Nino/ninos_images/indices_month_' + ano + mes + '_' + anoD + mesD + '_' + nino + '.png')
    fig.savefig('./Nino/ninos_images/intranet/indices_month_' + nino + '.png')

# -Loop de print. Todos juntos
fig, ax = plt.subplots(figsize=(10.80, 6.00), dpi=100)
for i in range(0, 4, 1):

    nino = grafico['Ninos'][i]
    anom = grafico['Anoms'][i]
    cor = grafico['Color'][i]
    subset = df[[anom, 'PDO']][str(data_ini):str(data_fim)]
    if subset[anom].max() > 2:
        L = 4
    else:
        L = 2

    subPrev = subset.dropna()[anom]

    ax.plot(pd.to_datetime(subPrev.index), subPrev, c=cor, linestyle='-')

# -Aqui separamos o loop pra ter uma legenda de apenas 4 elemetos
plt.legend(grafico['Ninos'], fontsize='small', loc='upper center',
           bbox_to_anchor=(0.5, 1.0), fancybox=True, shadow=True, ncol=4)

for i in range(0, 4, 1):
    nino = grafico['Ninos'][i]
    anom = grafico['Anoms'][i]
    cor = grafico['Color'][i]
    subset = df[[anom, 'PDO']][str(data_ini):str(data_fim)]

    subPrev = subset.dropna()[anom]
    subObs = subset[subset.isnull().any(axis=1)][anom]
    subObs = subObs.append(subPrev.iloc[[0]], ignore_index=False)

    ax.plot(pd.to_datetime(subObs.index), subObs, c=cor, linestyle='--')

ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%y"))
plt.title('Indice Ninos Observado X Previsao')
plt.ylim(-1 * L, L)
plt.ylabel('Anomalia de temp (C)')
plt.xticks(subset.index, rotation=45)
plt.grid(True)

plt.axhspan(0.5, L, facecolor='r', alpha=0.4)
plt.axhspan(-0.5, -1 * L, facecolor='b', alpha=0.4)
fig.savefig('./Nino/ninos_images/indices_month_' + ano + mes + '_' + anoD + mesD + '_all.png')
fig.savefig('./Nino/ninos_images/intranet/indices_month_all.png')

# ----------------------------------------------------
# --------------------------Season--------------------

try:
    arquivo = './Nino/ninos_data/sasonal.csv'
    df = pd.read_csv(arquivo, index_col=0)
except:
    arquivo = './ninos_data/sasonal.csv'
    df = pd.read_csv(arquivo, index_col=0)

df = pd.read_csv(arquivo, index_col=0)

# Ta no mesmo script pq tem coisas como datas sendo reutilizadas. Mas so isso msm
print('Graficos trimestrais')
for i in range(0, 4, 1):
    nino = grafico['Ninos'][i]
    anom = grafico['Anoms'][i]
    print(anom, nino)
    subset = df[[anom, 'meses']][str(data_ini):str(data_fim)]
    if subset[anom].max() > 2:
        L = 4
    else:
        L = 2

    # --Gera Imagem
    fig2, ax2 = plt.subplots(figsize=(10.80, 6.00), dpi=100)
    ax2.plot(pd.to_datetime(subset.index[:-9]), subset[anom][:-9], 'b--')
    ax2.plot(pd.to_datetime(subset.index[-10:]), subset[anom][-10:], 'b')

    # --Perfumaria do grafico
    ax2.set_xticks(pd.to_datetime(subset.index[-22:]))
    ax2.set_xticklabels(subset.meses[-22:], rotation=45)

    plt.title('Indice sasonal do ' + str(nino) + ' Observado X Previsao')
    plt.ylim(-1 * L, L)
    plt.grid(True)
    plt.ylabel('Anomalia de temp (C)')

    plt.axhspan(0.5, L, facecolor='r', alpha=0.4)
    plt.axhspan(-0.5, -1 * L, facecolor='b', alpha=0.4)
    fig2.savefig('./Nino/ninos_images/indices_season_' + ano + mes + '_' + anoD + mesD + '_' + nino + '.png')
    fig2.savefig('./Nino/ninos_images/intranet/indices_season_' + nino + '.png')

# -Loop de print. Todos juntos
fig, ax = plt.subplots(figsize=(10.80, 6.00), dpi=100)
for i in range(0, 4, 1):
    nino = grafico['Ninos'][i]
    anom = grafico['Anoms'][i]
    cor = grafico['Color'][i]
    subset = df[[anom, 'meses']][str(data_ini):str(data_fim)]
    if subset[anom].max() > 2:
        L = 4
    else:
        L = 2
    ax.plot(pd.to_datetime(subset.index[-10:]), subset[anom][-10:], c=cor, linestyle='-')

# -Aqui separamos o loop pra ter uma legenda de apenas 4 elemetos
plt.legend(grafico['Ninos'], fontsize='small', loc='upper center',
           bbox_to_anchor=(0.5, 1.0), fancybox=True, shadow=True, ncol=4)
for i in range(0, 4, 1):
    nino = grafico['Ninos'][i]
    anom = grafico['Anoms'][i]
    cor = grafico['Color'][i]
    subset = df[[anom, 'meses']][str(data_ini):str(data_fim)]
    if subset[anom].max() > 2:
        L = 4
    else:
        L = 2
    ax.plot(pd.to_datetime(subset.index[:-9]), subset[anom][:-9], c=cor, linestyle='--')

ax.set_xticks(pd.to_datetime(subset.index[-22:]))
ax.set_xticklabels(subset.meses[-22:], rotation=45)
plt.title('Indice trimestral Ninos Observado X Previsao')
plt.ylim(-1 * L, L)
plt.ylabel('Anomalia de temp (C)')
plt.grid(True)
plt.axhspan(0.5, L, facecolor='r', alpha=0.4)
plt.axhspan(-0.5, -1 * L, facecolor='b', alpha=0.4)
fig.savefig('./Nino/ninos_images/indices_season_' + ano + mes + '_' + anoD + mesD + '_all.png')
fig.savefig('./Nino/ninos_images/intranet/indices_season_all.png')

# scp *png operacao@somar1.dc.met.com.br:/p1/operacao/produtos/ENSO
# https://stackoverflow.com/questions/42684530/convert-a-column-in-a-python-pandas-from-string-month-into-int

# Mudar grafico de cor
# https://stackoverflow.com/questions/46213266/matplotlib-changing-line-color-above-below-hline/46220028


