
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
       
    # if (n%2)==0 and pot<0:
    #     pot=pot*(-1)

    return pot
#Fim da função que calcula expoente


#Função que aproxima cosseno:
def aproximacosseno(x,epsilon):

    #LEMBRAR DE LIMITAR O COSSENO ENTRE 0 E PI/2
   
    modulo_termo_anterior = 1

    termo_atual = (expoente(x,2))/2
    modulo_termo_atual = modulo(termo_atual)

    soma_cos = modulo_termo_anterior - termo_atual
    i=2

    print(f'Termo anterior {modulo_termo_anterior}')
    print(f'Termo atual {termo_atual}')
    print(f'epsilon {epsilon}')
    
    while (modulo_termo_anterior >= epsilon) and (modulo_termo_atual > epsilon):


        termo_atual = (((expoente(x,(2*i)))*(expoente(-1,i)))/(fatorial(2*i)))
        soma_cos = soma_cos + termo_atual #CONFERIR DEPOIS


        modulo_termo_anterior = modulo_termo_atual
        modulo_termo_atual = modulo(termo_atual) 

        '''talvez precise definir somacos como float, mas eu não sei fazer'''

        #somacos = somacos + ( (x^(2*i))*((-1)^(i)) )/(fat(i*2)) #CONFERIR NO CADERNO DEPOIS
        #aqui, no lugar de fat, chamar a função que calcula fatorial.
        #aqui, no lugar de ^, chamar a função que calcula o expoente.
                           
        i=i+1          
                   
    return soma_cos #Fim da função que aproxima cosseno                                  

#Função integral por retângulos
def integral_por_retangulos (k,e,d):
    #fazer o intervalo entre 0 e pi/2  - corrigir o usuário
    #isto aqui se faz no main?

    #integral de 0 a k de cos(x)dx pode ser aproximada para:
    #somatória de i=0 até i=k de d*(cos(x-(i*d))) - onde d é a variável que vai receber o valor de delta do enunciado

    i=1 #ver se precisa usar outra variável como contador, eu gosto de usar i hdsuahusahuas
   
    somaret=0

    while (i*d)<k: #conferir esta condição

        somaret= somaret + (d*(aproximacosseno(x-(i*d))))
        #conferir aqui - está chamando a função pra calcular cos(x)
       
        i=i+1

    return somaret      
#Fim da função integral por retângulos


def main():

    print('\nEncontrando um valor aproximado de cosseno\n')
    x = float(input('\nInforme o valor de X: '))
    epsilon = float(input('\nInforme o valor do parametro epsilon: '))

    varr=aproximacosseno(x, epsilon)
    print ('O cosseno eh ',varr) #eu tava testando isto

if __name__== "__main__":
    main()