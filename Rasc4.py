# Question 2.
# Competição de Métodos: Quem Encontra a Raiz Mais Rápido?
# Objetivo: Comparar o desempenho dos métodos de ponto fixo, Newton-Raphson e Secante em diferentes funções.

import math
#O metodo do ponto fixo[1]: devemos isolar funçao, ver a regra, e escolher o ponto
#φ(x) = x + A(x)f(x) ;  A(x*) != 0
#A partir disso, o problema de encontrar a raiz de f se torna o provlema de encontrar o RF de Q -> Q(x') =  x*
#processo convergente e divergente: Se |Q'(x*)| < 1, o processo é convergente; se |Q'(x*)| > 1, é divergente. A ordem de convergencia e linear.
#Teorema de condição de convergencia: seja φ(x) continua , com derivada f' e f'' contiuas no intervalo que contem a soluçao x* (x*=φ(X*))
# Seja X0 pertencente  ap intevalo e M um limitante de forma que |φ'(x)| <= M < 1 entao
#a) polinomio calculado x(+) =φ(xi)
#b) |xi - x*| -> 0 , ou seja, xi -> x*
#c) φ'(x*) != 0 -> seq e monotonica e convergente
#φ'(x*) = 0  e  f''(x*) != 0 -> seq e oscilante e convergente


#O metodo de newton-raphson consiste em usar a derivada da funçao, achar sua tangente, e usar a intersecção da tangente com o eixo x para achar a próxima aproximação da raiz.
# f'(x) = f(xi)/(xi - xi+1) -> xi+1 = xi - f(xi)/f'(xi)
#Teorema de convergencia: Se a função f, f' e f'' sao continuas no intervalo que contem sua raiz [a,b] e f' != - entao a ordem de convergencia e quadratica

#O metodo da secante e uma variaçao do metodo de newton, usando 2 pontod para calcular a derivada, para achar um terceiro mais proximo da raiz.
#xi+1 = xi - (xi-xi-1)f(xi)/(f(xi) - f(xi-1))
#Ordem de convergencia e 1 + (raiz de 5 - 1)/2 = 1.618 (convergencia super linear)

# Descrição da Tarefa:
# 1. Selecione pelo menos duas funções não lineares (ex.: f(x) = x^3 − 7x + 6 e f(x) = ln(x + 1) + x − 2).
# 2. Para cada função:
# • Aplique os métodos de ponto fixo (com φ(x) adequada), Newton-Raphson e Secante.
# • Registre número de iterações, erros absolutos e tempo de execução.
# 3. Monte um ranking de “eficiência” dos métodos.
# Entrega: Código, gráficos de convergência, tabela comparativa de tempo/iterações/precisão e relatório crítico.
import numpy as np

#f(x) = x^3 - 7x + 6 
def f(x, mode='float64'):
    if mode == 'math.trunc': 
        return math.trunc((x**3 - 7*x + 6)*10e3)/10e3 # Truncamento com 4 casas decimais
    
    elif mode == 'float32':
        return np.float32(x**3 - 7*x + 6)
    
    return x**3 - 7*x + 6

#f'(x) = 3*x**2 - 7
def df(x, mode='float64'):
    if mode == 'math.trunc': 
        return math.trunc((3*x**2 - 7)*10e3)/10e3 # Truncamento com 4 casas decimais
    
    elif mode == 'float32':
        return np.float32(3*x**2 - 7)
    
    return 3*x**2 - 7

#F''(x) = 6*x
def ddff(x, mode='float64'):
    if mode == 'math.trunc': 
        return math.trunc((6*x)*10e3)/10e3 # Truncamento com 4 casas decimais
    
    elif mode == 'float32':
        return np.float32(6*x)
    return 6*x

#Para comparaçao de erros:
Raizes = [1, 2, 3] 

# Ponto fixo:

def ponto_fixo(a, b, t, mode='float64'):

    it = 0
    e = float('inf')

    if mode == 'float64':
        x = float(a)
    elif mode == 'float32':
        x = np.float32(a)
    elif mode == 'math.trunc':
        x = math.trunc(a*10e3)/10e3

    
    while it < t and e > 1e-10:
        if mode == 'float64':
            p = x - f(x)/df(x)
        elif mode == 'float32':
            p = np.float32(x - f(x)/df(x))
        elif mode == 'math.trunc':
            p = math.trunc((x - f(x)/df(x))*10000)/10000

        e = abs(p - x)
        it += 1