import numpy as np
from difflib import SequenceMatcher as SM


#Your statements here

NOR = np.array(['NO','AP'])
SER = np.array(['SE','SP','RJ'])
SUL = np.array(['SU','PR','RS','SC'])

big = []
pcdRAW = np .genfromtxt('AP.txt', delimiter=';', dtype = 'S')
maesRAW = np .genfromtxt('AP2.txt', delimiter=';', dtype = 'S')
pcd = np.char.upper(pcdRAW)
maes = np.char.upper(maesRAW)
# [:,3] significa todas[:] as linhas, apenas a coluna[3]. 
#Isso pode devolver 1 valor ou um array deles. Depende ser for uma matrix ou não
#tambem pode ser escrito como [:][3]. Depende do numero de parametro

maes_list = maes[:,-3:-1]

for i in maes_list[:,0]:
    j = 0
    pcd_city = pcd[:,1][j]               
    m = SM(None, pcd_list, i).ratio()
    while m < 0.5:
        j +=1
        pcd_city = pcd [:,1][j] 
        m = SM(None, pcd_city, i).ratio()
    #Estou salvando nesta variavel um array as colunas [0,1,2,6,8] da linha J e adicionando o nome [i] à tabela pq sim tlg
    pcd_maes = np.insert(pcd[j,[0,1,2,6,8]], 1, i)
    
    big.append(pcd_maes)
    a = np.array(big)
   # print (pcd_maes)
    
    #print ('achamos', pcd_city, i, m)

#print a
print (a[np.where(a[:,3] == 'AP')][:,[1,4,5]])