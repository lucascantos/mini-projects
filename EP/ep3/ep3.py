## MUNDO

objetos = ['', 'P', 'W', 'O']

def le_mundo(file):
    with open(file, 'r', encoding='utf-8') as f:
        mundo = []
        index = 0
        for linha in f:
            if index == 0:
                N = int(linha)
                if N > 9:
                    print('N deve ser menor do que 9')
                    return False
            else: 
                # remove \n no final da linha
                linha = linha.strip()
                # separa caracteres pelo separador espaço e devolve uma lista
                item = linha.split(' ')
                items.append(item)
                print(item)
            index += 1
        return (N, items)


def adiciona_pontos(pontos):
    agente[3] = agente[3] + pontos

## AGENTE

def andar():
    adiciona_pontos(-1)
    '''
    0: linha
    1: coluna
    '''
    futuro = []
    futuro[0] = agente[0] + movimento[0]
    futuro[1] = agente[1] + movimento[1]
    if 0 <= futuro[0] <= N-1 or 0 <= futuro[1] <= N-1:
        agente[0] =  futuro[0]
        agente[1] =  futuro[1]
    else:
        # percepcao = 'C'

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
    estado[2] = 0


def morrer():
    adiciona_pontos(-1000)

def matar_wumpus()
    adiciona_pontos(50)

def atirar_flecha():


arquivo = 'entrada.txt'
N, items = mundo_wumpus(arquivo)

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

