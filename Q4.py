# Question 2.
# Competição de Métodos: Quem Encontra a Raiz Mais Rápido?
# Objetivo: Comparar o desempenho dos métodos de ponto fixo, Newton-Raphson e Secante em diferentes funções.

import math
import time
# Descrição da Tarefa:
# 1. Selecione pelo menos duas funções não lineares (ex.: f(x) = x^3 − 7x + 6 e f(x) = ln(x + 1) + x − 2).
# 2. Para cada função:
# • Aplique os métodos de ponto fixo (com φ(x) adequada), Newton-Raphson e Secante.
# • Registre número de iterações, erros absolutos e tempo de execução.
# 3. Monte um ranking de “eficiência” dos métodos.
# Entrega: Código, gráficos de convergência, tabela comparativa de tempo/iterações/precisão e relatório crítico.
import numpy as np

#f(x) = x^3 - 7x + 6 
def f(x): return x**3 - 7*x + 6

#f'(x) = 3*x**2 - 7
def df(x): return 3*x**2 - 7

#F''(x) = 6*x
def ddff(x): return 6*x


#Para comparaçao de erros:
Raizes = [1, 2, -3] 

# Ponto fixo:
#O método do ponto fixo: devemos isolar a função, ver a regra, e escolher o ponto
#φ(x) = x + A(x)f(x) ;  A(x*) != 0
#A partir disso, o problema de encontrar a raiz de f se torna o problema de encontrar o RF de Q -> Q(x') =  x*
#processo convergente e divergente: Se |Q'(x*)| < 1, o processo é convergente; se |Q'(x*)| > 1, é divergente. A ordem de convergencia e linear.
#Teorema de condição de convergência: seja φ(x) contínua , com derivada f' e f'' contínuas no intervalo que contém a solução x* (x*=φ(X*))
# Seja X0 pertencente ao intervalo e M um limitante de forma que |φ'(x)| <= M < 1 então
#a) polinomio calculado x(+) =φ(xi)
#b) |xi - x*| -> 0 , ou seja, xi -> x*
#c) φ'(x*) != 0 -> seq é monotônica e convergente
#φ'(x*) = 0  e  f''(x*) != 0 -> seq é oscilante e convergente

def phi(x): return (x**3 +6)/7
def dphi(x): return (3*x**2)/7

def ponto_fixo(x, t):
    name = "Ponto Fixo"
    it = 0
    e = [] 
    start_time = time.time()

    x.append(phi(x[0])) 

    while abs(x[it + 1] - x[it]) > t and it < 100: 
        e.append(min(abs(x[it] - Raizes[0]), abs(x[it] - Raizes[1]), abs(x[it] - Raizes[2]))) 
        it += 1
        
        x.append(phi(x[it]))

        if dphi(x[it-1]) < 1: 
            print("Processo convergente")
        elif dphi(x[it-1]) > 1:
            print("Processo divergente")

    tempo = time.time() - start_time
    return it, e, name, tempo

# Newton-Raphson:
#O método de newton-raphson consiste em usar a derivada da função, achar sua tangente, e usar a intersecção da tangente com o eixo x para achar a próxima aproximação da raiz.
# f'(x) = f(xi)/(xi - xi+1) -> xi+1 = xi - f(xi)/f'(xi)
#Teorema de convergência: Se a função f, f' e f'' são contínuas no intervalo que contém sua raiz [a,b] e f' != 0 então a ordem de convergência é quadrática
def newton(x, t):
    name = "Newton-Raphson"
    it = 0
    e = [] 
    start_time = time.time()

    x.append(x[0] - f(x[0])/df(x[0]))

    while abs(x[it + 1] - x[it]) > t and it < 100: 
        e.append(min(abs(x[it] - Raizes[0]), abs(x[it] - Raizes[1]), abs(x[it] - Raizes[2]))) 
        it += 1
        
        x.append(x[it] - f(x[it])/df(x[it]))

    tempo = time.time() - start_time
    return it, e, name, tempo
# Secante:

#O método da secante é uma variação do método de newton, usando 2 pontos para calcular a derivada, para achar um terceiro mais próximo da raiz.
#xi+1 = xi - (xi-xi-1)f(xi)/(f(xi) - f(xi-1))
#Ordem de convergencia e 1 + (raiz de 5 - 1)/2 = 1.618 (convergencia super linear)                  
def secante(x, t):
    name = "Secante"
    it = 0
    e = [] 
    start_time = time.time()


    while abs(x[it + 1] - x[it]) > t and it < 100: 
        e.append(min(abs(x[it+1] - Raizes[0]), abs(x[it+1] - Raizes[1]), abs(x[it+1] - Raizes[2]))) 
        
        novo_x = x[it+1] - (((x[it+1] - x[it]) * f(x[it+1])) / (f(x[it+1]) - f(x[it])))
        x.append(novo_x)
        
        it += 1

    tempo = time.time() - start_time
    
    return it, e, name, tempo

# Question 2.
# Competição de Métodos: Quem Encontra a Raiz Mais Rápido?
# Objetivo: Comparar o desempenho dos métodos de ponto fixo, Newton-Raphson e Secante em diferentes funções.

import math
import time
# Descrição da Tarefa:
# 1. Selecione pelo menos duas funções não lineares (ex.: f(x) = x^3 − 7x + 6 e f(x) = ln(x + 1) + x − 2).
# 2. Para cada função:
# • Aplique os métodos de ponto fixo (com φ(x) adequada), Newton-Raphson e Secante.
# • Registre número de iterações, erros absolutos e tempo de execução.
# 3. Monte um ranking de “eficiência” dos métodos.
# Entrega: Código, gráficos de convergência, tabela comparativa de tempo/iterações/precisão e relatório crítico.
import numpy as np

#f(x) = x^3 - 7x + 6 
def f(x): return x**3 - 7*x + 6

#f'(x) = 3*x**2 - 7
def df(x): return 3*x**2 - 7

#F''(x) = 6*x
def ddff(x): return 6*x


#Para comparaçao de erros:
Raizes = [1, 2, -3] 

# Ponto fixo:
#O método do ponto fixo: devemos isolar a função, ver a regra, e escolher o ponto
#φ(x) = x + A(x)f(x) ;  A(x*) != 0
#A partir disso, o problema de encontrar a raiz de f se torna o problema de encontrar o RF de Q -> Q(x') =  x*
#processo convergente e divergente: Se |Q'(x*)| < 1, o processo é convergente; se |Q'(x*)| > 1, é divergente. A ordem de convergencia e linear.
#Teorema de condição de convergência: seja φ(x) contínua , com derivada f' e f'' contínuas no intervalo que contém a solução x* (x*=φ(X*))
# Seja X0 pertencente ao intervalo e M um limitante de forma que |φ'(x)| <= M < 1 então
#a) polinomio calculado x(+) =φ(xi)
#b) |xi - x*| -> 0 , ou seja, xi -> x*
#c) φ'(x*) != 0 -> seq é monotônica e convergente
#φ'(x*) = 0  e  f''(x*) != 0 -> seq é oscilante e convergente

def phi(x): return (x**3 +6)/7
def dphi(x): return (3*x**2)/7

def ponto_fixo(x, t):
    name = "Ponto Fixo"
    it = 0
    e = [] 
    start_time = time.perf_counter() # perf_counter é mais preciso que time()

    while it < 100: 
    
        x_novo = phi(x[it])
        x.append(x_novo)
        it += 1
        
        e.append( min([abs(x[it] - r) for r in Raizes]) )

       
        if abs(x[it] - x[it-1]) < t: # evita que eu deixe de salvar o ultimo erro caso o critério de parada seja atingido
            break

    tempo = time.perf_counter() - start_time
    return it, e, name, tempo

# Newton-Raphson:
#O método de newton-raphson consiste em usar a derivada da função, achar sua tangente, e usar a intersecção da tangente com o eixo x para achar a próxima aproximação da raiz.
# f'(x) = f(xi)/(xi - xi+1) -> xi+1 = xi - f(xi)/f'(xi)
#Teorema de convergência: Se a função f, f' e f'' são contínuas no intervalo que contém sua raiz [a,b] e f' != 0 então a ordem de convergência é quadrática
def newton(x, t):
    name = "Newton-Raphson"
    it = 0
    e = [] 
    start_time = time.perf_counter()

    while it < 100: 
        if df(x[it]) == 0: break 
            

        x.append(x[it] - f(x[it])/df(x[it]))
        it += 1
        
       
        e.append(min([abs(x[it] - r) for r in Raizes]))

        if abs(x[it] - x[it-1]) < t:
            break
    
    tempo = time.perf_counter() - start_time
    return it, e, name, tempo


# Secante:

#O método da secante é uma variação do método de newton, usando 2 pontos para calcular a derivada, para achar um terceiro mais próximo da raiz.
#xi+1 = xi - (xi-xi-1)f(xi)/(f(xi) - f(xi-1))
#Ordem de convergencia e 1 + (raiz de 5 - 1)/2 = 1.618 (convergencia super linear)                  
def secante(x, t):
    name = "Secante"
    it = 1 
    e = [] 
    start_time = time.perf_counter()

    while it < 100: 
        
        if f(x[it]) - f(x[it-1]) == 0: break 
            
       
        x.append(x[it] - (((x[it] - x[it-1]) * f(x[it])) / (f(x[it]) - f(x[it-1]))))
        it += 1
        
        e.append(min([abs(x[it] - r) for r in Raizes]))

        if abs(x[it] - x[it-1]) < t:
            break

    tempo = time.perf_counter() - start_time
    return it, e, name, tempo

R = [ponto_fixo([0.5], 1e-5), newton([0.5], 1e-5), secante([0.5, 0.6], 1e-5)]
R.sort(key=lambda x: x[0]) # Ordena pelo número de iterações (do menor para o maior)


import matplotlib.pyplot as plt
import pandas as pd

data_struct = {
    'Posição': [1, 2, 3],
    'Método': [R[0][2], R[1][2], R[2][2]],
    'Iterações': [R[0][0], R[1][0], R[2][0]],
    'Erro Final': [R[0][1][-1] if R[0][1] else 0, R[1][1][-1] if R[1][1] else 0, R[2][1][-1] if R[2][1] else 0],
    'Tempo (s)': [f"{R[0][3]:.6e}", f"{R[1][3]:.6e}", f"{R[2][3]:.6e}"]
}

df_results = pd.DataFrame(data_struct)

print("\n RANKING DE EFICIÊNCIA")
print(df_results.to_string(index=False))

# Salvar em arquivo CSV com notação científica
df_results.to_csv('./ResultadosPY/resultados_q4.csv', index=False)
print("\nResultados salvos em 'resultados_q4.csv'")

plt.figure(figsize=(10, 6))

cores = {'Ponto Fixo': '#3498db', 'Newton-Raphson': '#2ecc71', 'Secante': '#e74c3c'}

for i in R:
    plt.plot(range(1, len(i[1]) + 1), i[1], marker='o', linewidth=2, label=i[2], color=cores[i[2]])
    # i[0] é o número de iterações, i[1] é a lista de erros, i[2] é o nome do método
plt.yscale('log') #dessa forma podemos ver o comportamento exponencial do erro, e comparar melhor a convergencia dos métodos
plt.xlabel('Número de Iterações')
plt.ylabel('Erro Absoluto')
plt.title('Competição de Convergência: f(x) = x³ - 7x + 6')
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.6)
plt.show()


# o x final nao e do interesse
# alguns dos metodos ultillizados podem retardar o tempo de cada metodo, uma vez que usamos os mesmo para todos faz com que na comparaçao isso nao seja um problema.