#------------------------------------------
#Nome: Julianna Freire Caravetto
#NºUSP: 7699020
#Versão Python: 3.6.8 64 bits
#EP3: Caça ao ouro no mundo do Wumpus
#MAC0115 - Professora Leliane Nunes de Barros
#------------------------------------------
'''
    Ao preencher esse cabeçalho com o meu nome e o meu número USP,
    declaro que todas as partes originais desse exercício programa (EP)
    foram desenvolvidas e implementadas por mim e que portanto não
    constituem desonestidade acadêmica ou plágio.
    Declaro também que sou responsável por todas as cópias desse
    programa e que não distribui ou facilitei a sua distribuição.
    Estou ciente que os casos de plágio e desonestidade acadêmica
    serão tratados segundo os critérios divulgados na página da
    disciplina.
    Entendo que EPs sem assinatura devem receber nota zero e, ainda
    assim, poderão ser punidos por desonestidade acadêmica.

    Busquei ajuda nos seguintes sites:
   
    https://panda.ime.usp.br/aulasPython/static/aulasPython/index.html
Aulas de Introdução à Computação em Python — Aulas de Introdução à Computação com Python: Edição Interativa - Panda
Versão interativa das aulas de Introdução à Computação com Python.
panda.ime.usp.br

    #para informações gerais sobre os novos tópicos vistos em aula.

    A lógica de programação foi feita num caderno, me comprometo a apresentar
    caso seja necessario.

'''

## ----- MUNDO

objetos_label = [' ', 'P', 'W', 'O']

def le_mundo(mundo):
    # Abre o arquivo de entrada localizado na mesma pasta do programa.
    # Cria um mundo e preenche ele com os objetos tipo Wumpus e Poços
    file = 'entrada.txt'
    with open(file, 'r') as f:
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
    if 0 <= ponto[0] <= N-1 and 0 <= ponto[1] <= N-1:
        return True
    else:
        return False

def imprime_mundo(matrix):
    # Imprime Mundo para o usuário visualizar
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

percebe_label = ['F', 'B', 'R', 'C', 'U'] # O que o agente sente ao andar pelas salas.

def atualiza_percepcaoEagente(percebe, mundo, acao, agente, estado):
    # Atualiza percepções e a posição do agente
    acoes(acao)
    check_objetos(mundo)
    text = ''
    for i in percepcao[:3]:
       text += str(i)
    percebe[agente[0]][agente[1]] = text
    
    ultimo_percebe = limpa_percepcao()
    
    if agente[2] != 'x' and agente[0] != -1:
        print('Percepção após a última ação:')
        print('['+ultimo_percebe+']')
        print('Mundo conhecido pelo agente:')
        imprime_percebe(percebe)


def check_objetos(mundo):
    # olhar o que esta na sala atual
    sala = mundo[agente[0]][agente[1]]
    if sala != 0: # Se a sala não estiver vazia
        if (sala == 1 and estado[0]==1) or sala == 2: # Se na sala tiver um poço ou o Wumpus
            morrer()
        if sala == 3: # Se na sala tiver ouro
            percepcao[2] = 1
           
    check_vizinho([agente[0], agente[1]])

def check_vizinho(ponto):
    # Percepções em volta:
    n = [ponto[0]-1, ponto[1]]
    s = [ponto[0]+1, ponto[1]]
    l = [ponto[0], ponto[1]+1]
    o = [ponto[0], ponto[1]-1]

    vizinhos = [n, s, l, o]
    for vizinho in vizinhos:
        if outbound(vizinho): # Se local vizinho está dentro da caverna
            # Ver se percebe algum perigo em volta:
            if mundo[vizinho[0]][vizinho[1]] == 1:
                percepcao[1] = 1
            elif mundo[vizinho[0]][vizinho[1]] == 2:
                percepcao[0] = 1  

def limpa_percepcao():
    index=0
    text = ''
    for i in percepcao:
        if i == 1:
            text += percebe_label[index]
        percepcao[index] = 0
        index+=1
    return text


def imprime_percebe(matrix):
    # Imprime percepções ao longo do jogo
    # Para que o usuário se oriente durante a movimentação
    # Atualiza o mapa durante a movimentação
   
    mapa_impresso=''
    for i in range(N):
        for j in range(N):
            mapa_impresso += '-------'
        mapa_impresso += '\n'
        for j in range(N):
            if agente[0] == i and agente[1] == j:

                texto = agente[2]
            else:
                texto = ' '
            index = 0
            data = matrix[i][j]
            for k in data:
                if k == '1':
                    texto += percebe_label[index]
                elif k =='0':
                    texto += ' '
                elif k == '?' or k == ' ':
                    texto = ' '+k+'  '
                index+=1

            mapa_impresso += '| '+texto+' '

        mapa_impresso += '|\n'    
    for j in range(N):
        mapa_impresso += '-------'
    print(mapa_impresso)
           

## AGENTE

def acoes(comando):
    # Ações do agente:
    if comando == 'D' or comando =='E':
        girar(comando)
    elif comando == 'M':
        mover()
    elif comando == 'T':
        atirar_flecha()
    elif comando == 'G':
        pegar_ouro()
    elif comando == 'S':
        sair()
    elif comando == '':
        pass
    else:
        print("Comando invalido!")


def mover():
    # Pontuação por mover:
    adiciona_pontos(-1)
    '''
    0: linha
    1: coluna
    '''
    # Próxima posição:
    futuro = [agente[0], agente[1]]
    futuro[0] = agente[0] + movimento[0]
    futuro[1] = agente[1] + movimento[1]
    if outbound(futuro):
        agente[0] =  futuro[0]
        agente[1] =  futuro[1]
    else:
        percepcao[3] = 1

def girar(acao):
    adiciona_pontos(-1)  
    orientacao = agente[2]
    # Orientar movimentação
    if acao == 'D':
        if orientacao == '>':
            orientacao = 'v'
            direcao = [1, 0]            
        elif orientacao == 'v':
            orientacao = '<'
            direcao = [0, -1]  
        elif orientacao == '<':
            orientacao = '^'
            direcao = [-1, 0]
        elif orientacao == '^':
            orientacao = '>'
            direcao = [0, 1]  
   
    elif acao == 'E':
        if orientacao == '>':
            orientacao = '^'
            direcao = [-1, 0]  
        elif orientacao == 'v':
            orientacao = '>'
            direcao = [0, 1]  
        elif orientacao == '<':
            orientacao = 'v'
            direcao = [1, 0]  
        elif orientacao == '^':
            orientacao = '<'
            direcao = [0, -1]  
   
    agente[2] = orientacao
    movimento[0] = direcao[0]
    movimento[1] = direcao[1]

def pegar_ouro():
    # Se o ouro exitir, muda o estado do ouro, se nao perde 1 ponto
    if estado[2] == 1 and percepcao[2] == 1:
        print('Kaching!')
        estado[2] = 0
    else:
        print('Sem ouro por aqui.')
        adiciona_pontos(-1)

def atirar_flecha():
    # Verifica se atirou a flecha no local certo (se o Wumpus morre)
    if estado[1] == 1:
        estado[1]=0
        print('Flecha atirada!')
    pass

def sair():
    # Orientações para sair da caverna
    if agente[0]==N-1 and agente[1]==0:
        game_over()
    else:
        print('Não há saida nesta sala')
        adiciona_pontos(-1)

def morrer():
    # Pontuação após morte
    
    print('AAAHHH...O agente morreu!')
    agente[2] = 'x'
    adiciona_pontos(-10000)
    game_over()

def matar_wumpus():
    # Pontuação após matar o Wumpus
    estado[0] = 0
    adiciona_pontos(50)

def adiciona_pontos(pontos):
    # Cálculo dos pontos durante e ao final do jogo
    estado[3] = estado[3] + pontos

def game_over():
    if estado[2] == 0:
        adiciona_pontos(100)
    agente[0] = -1
    print('Mundo Completo:')
    imprime_mundo(mundo)    
    print('Fim de Jogo! Pontuação final: '+str(estado[3]))
    return False

mundo = []
percebe = []

N, items = le_mundo(mundo)
cria_matrix(percebe,N,'?')
'''
0: Status do monstro
1: Status da flecha
2: Status do Ouro
3: pontucao
'''
estado = [1, 1, 1, 0]

'''
0: posição x
1: posição y
2: orientação de visão
'''
agente = [N-1, 0, '^']
movimento = [-1, 0]

percepcao = [0,0,0,0,0]


def main():
    # Códigos da função main
    
    
    atualiza_percepcaoEagente(percebe, mundo, '', agente, estado)
    while agente[2] != 'x' and agente[0] != -1:
        acao = input('Digite uma ação (M/E/D/T/G/S): ')        
        atualiza_percepcaoEagente(percebe, mundo, acao.upper(), agente, estado)

   

#fim da função main


if __name__== "__main__":   #chama a função main para rodar o EP
    main()

input() #Ao abrir o EP no Python, só fecha a janela apertando enter.
#Fim.