

class Func1:
    def f(self, x): return x**3 - 7*x + 6
    #f'(x) = 3*x**2 - 7
    def df(self, x): return 3*x**2 - 7
    #Para comparaçao de erros:
    Raizes = [1, 2, -3] 
    def phi(self, x): return (x**3 +6)/7
    def dphi(self, x): return (3*x**2)/7

class Func2:
    def g(self, x): return math.log(x + 1) + x - 2
    def dg(self, x): return 1/(x + 1) + 1
    Raizes = [1.20794] 

    def phi_g(self, x): return 2 - math.log(x + 1)
    def dphi_g(self, x): return -1/(x + 1)

g = 9.81
L = 1
T = 2.0 #Período observado arbitrário.

import math
Raizes = math.asin((T / (2 * math.pi)) * math.sqrt(g / L))
#print(Raizes) #asin me rtorna o resultado no primeiro quadrante, ou seja, a menor raiz.


import math
import numpy as np
a = math.log(2) 
#print(a)
#print(np.float32(a))




def f(x, mode='float64'):
    if mode == 'math.trunc': 
        return math.trunc(((math.exp(x)) - 2)*10e3)/10e3 # Truncamento com 4 casas decimais
    
    elif mode == 'float32':
        return np.float32(np.exp(x) - 2)
    
    return math.exp(x) - 2 # Valor em float64 por padrão, que é a precisão normal do Python.

# f(x) =  e^x - 2 ->  x * log(e) = log(2) -> x = log(2) -> raiz = log(2)
raiz = math.log(2) # raiz exata para comparação de erros
(a,b,t) = -2, 2, 0.0000000000000001



# Método de bisseção
# Selecionamos extremos em uma função que garantam a existência de uma raiz entre eles, tal que f(a) e f(b) tenham sinais opostos. Pelo Teorema de Bolzano (Seção 2.1 [1] e Seção de revisão em cálculo 1.1 [2]), podemos garantir que, se o produto das funções for menor que zero, haverá ao menos uma raiz entre esses dois pontos.
# [1] x^(k) = [a^(k) + b^(k)] / 2

def bissecao(a, b, t, mode='float64'): # aqui eu apenas juntei todas as 3 contas em um definidor, para poder facilmente mudar os parâmetros.
    # Aqui a, b e t são os parâmetros de entrada, e mode determina a precisão utilizada (float64, float32 ou truncamento).
    it = 0 # contador de iterações
    e = [] # lista para armazenar os erros em cada iteração, para análise posterior.


    while abs(b - a) > t and it < 100: # (critério de parada 1 e 2)
        #Parametros iniciais:
        x = (a + b) / 2 # Equação da bisseção para calcular o ponto médio entre a e b.
        it +=1

        #Garantir precisao do resultado:
        if mode == 'math.trunc': # Se escolhermos o modo de truncamento, aplicamos a função de truncamento ao x (resultado da bisseção) para simular a perda de precisão.
            x = math.trunc(x * 10e3) / 10e3
        elif mode == 'float32': # Se escolhermos o modo de float32, convertemos x para float32 para simular a precisão reduzida.
            x = np.float32(x)
        elif mode == 'float64': # Redundância para garantir que o modo float64 seja aplicado, embora seja o padrão.
            pass
        
        e.append(float(abs(x - raiz))) # Armazena o erro absoluto em relação à raiz exata para análise de convergência.

        if f(x, mode) == 0: # Observa se encontramos a raiz exata, o que é improvável, mas possível.
            return x
        
        elif f(a, mode) * f(x, mode) < 0: # Regra de Bolzano, acompanhada do modo de precisão selecionado.
            b = x # Se a função muda de sinal entre a e x, então a raiz está entre a e x, b desce para x.

        else:
            a = x # Caso contrário, a raiz está entre x e b, então a sobe para x.

    return x # Retorna a aproximação da raiz e o número de iterações realizadas.


print(bissecao(a,b,t, mode='float32')) # a = -2, b = 2, t = 10e3, modo float64