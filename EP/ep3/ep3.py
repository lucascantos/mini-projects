## ----- MUNDO

objetos_label = [' ', 'P', 'W', 'O']

def le_mundo(mundo):
    # Abre o arquivo de entrada localizado na mesma pasta do programa.
    # Cria um mundo e preenche ele com os objetos tipo Wumpus e Poços
    file = 'entrada.txt'
    with open(file, 'r', encoding='utf-8') as f:
        items = []
        index = 0
        for linha in f:
            if index == 0:
                N = int(linha)
                cria_matrix(mundo, N)

                if N > 9:
                    print('N deve ser menor do que 9.')
                    return False
            else: 
                # remove \n no final da linha
                linha = linha.strip()
                # separa caracteres pelo separador espaço e devolve uma lista
                item = linha.split(' ')
                items.append(item)
                x = int(item[0])-1
                y = int(item[1])-1
                mundo[x][y] = int(item[2])
            index += 1        
        return N, items

def cria_matrix(matrix, N, fill=0):
    # Cria uma matriz NxN preenchida com zeros
    for i in range(N):
        linha = []
        for j in range(N):
            linha.append(fill)
        matrix.append(linha)
    return matrix

def outbound(ponto):
    # Checa se o ponto escolhido se encontra dentro do mundo
    if 0 <= ponto[0] <= N-1 or 0 <= ponto[1] <= N-1:
        return True
    else:
        return False

def imprime_mundo(matrix):
    mapa_impresso=''
    for i in range(N):
        for j in range(N):
            mapa_impresso += '----'
        mapa_impresso += '\n'
        for j in range(N):
            mapa_impresso += '| '+str(objetos_label[matrix[i][j]])+' '
        mapa_impresso += '|\n'
    
    for j in range(N):
        mapa_impresso += '----'
    print(mapa_impresso)





## PERCEPCOES

percebe_label = ['F', 'B', 'R']

def atualiza_percepcaoEagente(percebe, mundo, acao, agente, estado):
    acoes(acao)
    check_objetos(mundo)
    text = ''
    for i in percepcao[:3]:
       text += str(i)
    percebe[agente[0]][agente[1]] = text


def check_objetos(mundo):
    sala = mundo[agente[0]][agente[1]]
    if sala != 0:
        if sala == 1 or sala == 2:
            morrer()
        if sala == 3:
            percepcao[2] = 1
            
    check_vizinho([agente[0], agente[1]])

def check_vizinho(ponto):
    
    n = [ponto[0]-1, ponto[1]]
    s = [ponto[0]-1, ponto[1]]
    l = [ponto[0], ponto[1]+1]
    o = [ponto[0], ponto[1]-1]

    vizinhos = [n, s, l, o]

    for vizinho in vizinhos:
        if outbound(vizinho):
            if mundo[vizinho[0]][vizinho[1]] == 1:
                percepcao[1] = 1
            elif mundo[vizinho[0]][vizinho[1]] == 2:
                percepcao[0] = 1           

def imprime_percebe(matrix):
    
    mapa_impresso=''
    for i in range(N):
        for j in range(N):
            mapa_impresso += '------'
        mapa_impresso += '\n'
        for j in range(N):

            if agente[0] == i and agente [1==j]:
                texto = agente[2]
            else:
                texto = ' '
            index = 0
            data = matrix[i][j]
            for k in data:
                if k == '1':
                    texto += percebe_label[index]
                elif k == '?' or k == ' ':
                    texto = k 
                index+=1


            mapa_impresso += '| '+texto+' '

        mapa_impresso += '|\n'    
    for j in range(N):
        mapa_impresso += '------'
    print(mapa_impresso)
            

## AGENTE

def acoes(comando):
    if comando == 'D' or comando =='E':
        girar(movimento, comando)
    elif comando == 'M':
        mover()
    elif comando == 'T':
        atirar_flecha()
    elif comando == 'G':
        pegar_ouro()
    elif comando == 'S':
        sair()


def mover():
    adiciona_pontos(-1)
    '''
    0: linha
    1: coluna
    '''
    futuro = [agente[0], agente[1]]
    print(agente[0], movimento[0])
    futuro[0] = agente[0] + movimento[0]
    futuro[1] = agente[1] + movimento[1]
    if outbound(futuro):
        agente[0] =  futuro[0]
        agente[1] =  futuro[1]
    else:
        percepcao[3] = 1

def girar(orientacao, acao):
    adiciona_pontos(-1)  

    if acao == 'D':
        if orientacao == '>':
            orientacao = 'v'
            movimento = [1, 0]            
        elif orientacao == 'v':
            orientacao = '<'
            movimento = [0, -1]   
        elif orientacao == '<':
            orientacao = '^'
            movimento = [-1, 0] 
        elif orientacao == '^':
            orientacao = '>'
            movimento = [0, 1]  
    
    elif acao == 'E':
        if orientacao == '>':
            orientacao = '^'
            movimento = [-1, 0]  
        elif orientacao == 'v':
            orientacao = '>'
            movimento = [0, 1]  
        elif orientacao == '<':
            orientacao = 'v'
            movimento = [1, 0]  
        elif orientacao == '^':
            orientacao = '<'
            movimento = [0, -1]  
    
    agente[2] = orientacao
    return movimento

def pegar_ouro():
    # Se o ouro exitir, muda o estado do ouro, se nao perde 1 ponto
    estado[2] = 0

def atirar_flecha():
    pass

def sair():
    pass

def morrer():
    adiciona_pontos(-10000)

def matar_wumpus():
    adiciona_pontos(50)

def adiciona_pontos(pontos):
    estado[3] = estado[3] + pontos

mundo = []
percebe = []
percepcao = [0,0,0,0,0]
N, items = le_mundo(mundo)
cria_matrix(percebe,N,'?')

'''
0: posição x
1: posição y
2: orientação de visão
'''
agente = [N, 0, '^']
movimento = [-1, 0]



'''
0: Status do monstro
1: Status da flecha
2: Status do Ouro
3: pontucao
'''
estado = [1, 1, 1, 0]

for i in range(3):
    atualiza_percepcaoEagente(percebe, mundo, 'M', agente, estado) 

    print(estado[3])
    imprime_percebe(percebe)