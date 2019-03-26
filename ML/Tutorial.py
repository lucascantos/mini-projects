# https://www.youtube.com/watch?v=OGxgnH8y2NM&list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v
#Regretion 2

import pandas as pd
import quandl, math
import numpy as np
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression

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
forecast_out = int(math.ceil(0.01*len(df)))
print(forecast_out)

#Labels. Shift = move o conjunto de dados para cima(Negativamente)
#O Close é como fechou no dia anterior e como abriu no dia. O Label(Aresposta certa) nada mais é do que o Close do dia seguinte(ou o quanto pra frente vc quiser)
df['label'] = df[forecast_col].shift(-forecast_out)

df.dropna(inplace=True)
#X = Dados processados, menos o Label. y = label dos dados processados
X = np.array(df.drop(['label'], 1))
X_lately = X[-forecast_out]

y = np.array(df['label'])

#Separa X e y de maneira aleatoria em 20%
X_train,X_test, y_train, y_test = model_selection.train_test_split(X,y,test_size=0.2)

#Aqui começa. Usando Regressao Linear
clf = LinearRegression()
clf.fit(X_train, y_train)
#isso é o Erro Quadratico
accuracy = clf.score(X_test,y_test)

print(accuracy)