
#Função que calcula fatorial:
def fatorial (fat):
       
    fator=fat

    while fat>1:

        fator=fator*(fat-1)

        fat=fat-1

    return fator
#Fim da função que calcula o fatorial de um número.

#Função que faz o módulo de um número:
def modulo(mod):

    if mod < 0:
        mod=mod*(-1)
       
    return mod
#Fim da função que calcula o módulo de um número.

#Função que calcula expoente:
def expoente (x,n):
    #Fazendo x^n

    pot=1
    i=1

    while i <= n:
        pot=pot*x
        i=i+1

    return pot
#Fim da função que calcula expoente


#Função que aproxima cosseno:
def aproximacosseno(x, epsilon):

    #LEMBRAR DE LIMITAR O COSSENO ENTRE 0 E PI/2
   
    # primeiro termo da serie de taylor. modulo de 1 é 1
    modulo_termo_anterior = 1

    # calcula modulo do segundo da serie de taylor.
    termo_atual = (expoente(x,2))/2
    modulo_termo_atual = modulo(termo_atual)

    # soma dos primeiros dois termos da serie de taylor
    soma_cos = modulo_termo_anterior - termo_atual
    
    # indice do segundo termo da serie de taylor, que começa em 0
    p=1

    # caso os modulos fique entre os valores de epsilon
    while (modulo_termo_anterior >= epsilon) and (modulo_termo_atual > epsilon):
        p=p+1 

        # Calcula o valor do proximo fator da serie de taylor e soma na soma de cosseno
        termo_atual = (((expoente(x,(2*p)))*(expoente(-1,p)))/(fatorial(2*p)))
        soma_cos = soma_cos + termo_atual #CONFERIR DEPOIS

        # calcula o modulo dos proximos termos para atualizar o loop
        modulo_termo_anterior = modulo_termo_atual
        modulo_termo_atual = modulo(termo_atual) 
                        
    return soma_cos, p #Fim da função que aproxima cosseno                                  

#Função integral por retângulos
def integral_por_retangulos (k, delta, epsilon):
    #fazer o intervalo entre 0 e pi/2  - corrigir o usuário
    #isto aqui se faz no main?

    n=0 
   
    somaret=0

    while (n*delta)<=k: #conferir esta condição

        valor_cosseno, p = aproximacosseno((k-(n*delta)), epsilon) #p existe para guardar o resultado de i

        somaret = somaret + (delta * valor_cosseno)
        #conferir aqui - está chamando a função pra calcular cos(x)
       
        n=n+1

    return somaret, n-1, p      
#Fim da função integral por retângulos

#Função aproximação suficiente
def aproximacao_suficiente(k, epsilon, delta, psi):
    # Aproxima integral usando psi como controle de qualidade

    # calcula integral usando o delta dado e a integral com o expoente 2
    m = 1
    integral_anterior, n_anterior, p_anterior=integral_por_retangulos(k, delta, epsilon)
    novo_delta = delta/expoente(2, m)
    integral_atual, n_atual, p_atual=integral_por_retangulos(k, novo_delta, epsilon)


    # faz a diferença entre as integrais
    integral_dif = integral_anterior - integral_atual


    # enquanto o modulo da diferença for menor que psi, repete o precesso
    while modulo(integral_dif) >= psi:
        m = m+1
        # integral anterior é atualizada
        integral_anterior = integral_atual

        # nova integral é atualizada usando o novo valor de delta
        novo_delta = delta/expoente(2, m)
        # cada variavel recebe a saida da função
        integral_atual, n_atual, p_atual = integral_por_retangulos(k, novo_delta, epsilon)

        #calcula nova diferença entre integrais
        integral_dif = integral_anterior - integral_atual
    return integral_atual, m, n_atual, p_atual


def main():

    print('Ola')
    k = float(input('\nDigite o valor de k (limite de integracao): '))

    while k<0 or k>1.5707963267948: #0 <= k <= pi/2
        print('\nPor favor, digite k entre 0 e pi/2:')
        k = float(input('\nDigite o valor de k (limite de integracao): '))

    epsilon = float(input('\nDigite o valor do parametro epsilon (erro maximo da funcao cosseno): '))
    delta=float(input('\nDigite o intervalo de aproximacao de integracao delta: '))
    psi=float(input('\nDigite o valor de psi para o erro maximo de aproximacao da integral: '))

    varr=aproximacao_suficiente(k, epsilon, delta, psi)
    print('\nFeitos os calculos!')
    print('\nO valor aproximado para a integral eh de ', varr[0])

    print('\nOs valores que produziram a aproximacao foram: ')
    print ('m =',varr[1],' isto eh, intervalos de comprimentos d/2^', varr[1])
    print ('n =',varr[2],' retangulos bem pequenos')
    print ('p =',varr[3],' ultimo valor da aproximacao do cosseno')

if __name__== "__main__":
    main()

input('Fim do EP2')