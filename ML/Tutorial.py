# https://www.youtube.com/watch?v=OGxgnH8y2NM&list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v
#Regretion 2

import pandas as pd
import quandl, math, datetime
import numpy as np
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

style.use('ggplot')

df = quandl.get('WIKI/GOOGL')
#Colunas Importantes do Dataframe
df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]

#Porcentagem Calculada
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100

#Features do Negocio
df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]


forecast_col = 'Adj. Close'
df.fillna(-99999, inplace=True)
#Quanto dias vai ser previsão. 3000 = previsão para os proximos 30 dias
forecast_out = int(math.ceil(0.01*len(df)))
print(forecast_out)

#Labels. Shift = move o conjunto de dados para cima(Negativamente)
#O Close é como fechou no dia anterior e como abriu no dia. O Label(Aresposta certa) nada mais é do que o Close do dia seguinte(ou o quanto pra frente vc quiser)
df['label'] = df[forecast_col].shift(-forecast_out)

#X = Dados processados, menos o Label. y = label dos dados processados
X = np.array(df.drop(['label'], 1))
X = preprocessing.scale(X)
X = X[:-forecast_out]
X_lately = X[-forecast_out:]

df.dropna(inplace=True)
y = np.array(df['label'])

#Separa X e y de maneira aleatoria em 20%
X_train,X_test, y_train, y_test = model_selection.train_test_split(X,y,test_size=0.2)

#Aqui começa. Usando Regressao Linear
clf = LinearRegression(n_jobs=-1)
clf.fit(X_train, y_train)
with open('output/linearregression.pickle', 'wb') as f:
    pickle.dump(clf,f)

pickle_in = open('output/linearregression.pickle', 'rb')
clf = pickle.load(pickle_in)

#isso é o Erro Quadratico
accuracy = clf.score(X_test,y_test)

forecast_set = clf.predict(X_lately)
print(forecast_set, accuracy, forecast_out)

#preparando pra plotar
'''
Pega o ultimo valor, faz um timestamp, adiciona 86400 segundos e soma.  
'''
df['Forecast'] = np.nan
last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

# Pra cada valor previsto, somar 1 dia,
for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]
df['Adj. Close'].plot()
df['Forecast'].plot()
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()