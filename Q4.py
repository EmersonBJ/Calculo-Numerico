
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

class Func1:
    def f(self, x): return x**3 - 7*x + 6
    #f'(x) = 3*x**2 - 7
    def df(self, x): return 3*x**2 - 7
    #Para comparaçao de erros:
    Raizes = [1, 2, -3] 
    def phi(self, x): return (x**3 +6)/7
    def dphi(self, x): return (3*x**2)/7

class Func2:
    def f(self, x): return math.log(x + 1) + x - 2
    def df(self, x): return 1/(x + 1) + 1
    Raizes = [1.20794] 

    def phi(self, x): return 2 - math.log(x + 1)
    def dphi(self, x): return -1/(x + 1)

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


def ponto_fixo(x, t, func = Func1):
    name = "Ponto Fixo"
    it = 0
    e = [] 
    start_time = time.perf_counter() # perf_counter é mais preciso que time()

    while it < 100: 
    

        x.append(func.phi(x[it]))
        it += 1
        
        e.append( min([abs(x[it] - r) for r in func.Raizes]) )

       
        if abs(x[it] - x[it-1]) < t: # evita que eu deixe de salvar o ultimo erro caso o critério de parada seja atingido
            break

    tempo = time.perf_counter() - start_time
    return it, e, name, tempo

# Newton-Raphson:
#O método de newton-raphson consiste em usar a derivada da função, achar sua tangente, e usar a intersecção da tangente com o eixo x para achar a próxima aproximação da raiz.
# f'(x) = f(xi)/(xi - xi+1) -> xi+1 = xi - f(xi)/f'(xi)
#Teorema de convergência: Se a função f, f' e f'' são contínuas no intervalo que contém sua raiz [a,b] e f' != 0 então a ordem de convergência é quadrática
def newton(x, t, func = Func1):
    name = "Newton-Raphson"
    it = 0
    e = [] 
    start_time = time.perf_counter()

    while it < 100: 
        if func.df(x[it]) == 0: break 
            

        x.append(x[it] - func.f(x[it])/func.df(x[it]))
        it += 1
        
       
        e.append(min([abs(x[it] - r) for r in func.Raizes]))

        if abs(x[it] - x[it-1]) < t:
            break
    
    tempo = time.perf_counter() - start_time
    return it, e, name, tempo


# Secante:

#O método da secante é uma variação do método de newton, usando 2 pontos para calcular a derivada, para achar um terceiro mais próximo da raiz.
#xi+1 = xi - (xi-xi-1)f(xi)/(f(xi) - f(xi-1))
#Ordem de convergencia e 1 + (raiz de 5 - 1)/2 = 1.618 (convergencia super linear)                  
def secante(x, t, func = Func1):
    name = "Secante"
    it = 1 
    e = [] 
    start_time = time.perf_counter()

    while it < 100: 
        
        if func.f(x[it]) - func.f(x[it-1]) == 0: break 
            
       
        x.append(x[it] - (((x[it] - x[it-1]) * func.f(x[it])) / (func.f(x[it]) - func.f(x[it-1]))))
        it += 1
        
        e.append(min([abs(x[it] - r) for r in func.Raizes]))

        if abs(x[it] - x[it-1]) < t:
            break

    tempo = time.perf_counter() - start_time
    return it, e, name, tempo

R = [ponto_fixo([0.5], 1e-5, Func1()), newton([0.5], 1e-5, Func1()), secante([0.5, 0.6], 1e-5, Func1())]
S = [ponto_fixo([0.5], 1e-5, Func2()), newton([0.5], 1e-5, Func2()), secante([0.5, 0.6], 1e-5, Func2())]


import matplotlib.pyplot as plt
import pandas as pd

R.sort(key=lambda x: x[0]) 
S.sort(key=lambda x: x[0])  # Ordena pelo número de iterações (do menor para o maior)

#Func1
data_struct_R = {
    'Posição': [1, 2, 3],
    'Método': [R[0][2], R[1][2], R[2][2]],
    'Iterações': [R[0][0], R[1][0], R[2][0]],
    'Erro Final': [R[0][1][-1] if R[0][1] else 0, R[1][1][-1] if R[1][1] else 0, R[2][1][-1] if R[2][1] else 0],
    'Tempo (s)': [f"{R[0][3]:.6e}", f"{R[1][3]:.6e}", f"{R[2][3]:.6e}"]
}


#Func2
data_struct_S = {
    'Posição': [1, 2, 3],
    'Método': [S[0][2], S[1][2], S[2][2]],
    'Iterações': [S[0][0], S[1][0], S[2][0]],
    'Erro Final': [S[0][1][-1] if S[0][1] else 0, S[1][1][-1] if S[1][1] else 0, S[2][1][-1] if S[2][1] else 0],
    'Tempo (s)': [f"{S[0][3]:.6e}", f"{S[1][3]:.6e}", f"{S[2][3]:.6e}"]
}


print("\n=== RANKING DE EFICIÊNCIA: f(x) = x³ - 7x + 6 ===")
print(pd.DataFrame(data_struct_R).to_string(index=False))
pd.DataFrame(data_struct_R).to_csv('./ResultadosPY/Q4.1.csv', index=False)

print("\n=== RANKING DE EFICIÊNCIA: f(x) = ln(x + 1) + x - 2 ===")
print(pd.DataFrame(data_struct_S).to_string(index=False))
pd.DataFrame(data_struct_S).to_csv('./ResultadosPY/Q4.2.csv', index=False)

cores = {
    'Ponto Fixo': '#6D7B8D',
    'Newton-Raphson': '#73822B',
    'Secante': '#9C6241'
}

fig, axes = plt.subplots(1, 2, figsize=(14, 6)) 

for ax, resultados, titulo in zip(axes, [R, S], ['f(x) = x³ - 7x + 6', 'f(x) = ln(x + 1) + x - 2']):
    
    
    for i in resultados:
        ax.plot(range(1, len(i[1]) + 1), i[1], 
                marker='o', markersize=8, linewidth=2.5, 
                label=i[2], color=cores[i[2]],
                markeredgecolor='black', markeredgewidth=1.5) 
        
    ax.set_yscale('log') 
    ax.set_xlabel('Número de Iterações', fontweight='bold', color='#2c3e50')
    ax.set_ylabel('Erro Absoluto', fontweight='bold', color='#2c3e50')
    ax.set_title(f'{titulo}', fontweight='bold', fontsize=14, color='#2c3e50')
    ax.legend(framealpha=0.9, edgecolor='black')
    ax.grid(True, which="both", ls="--", color='#57606f', alpha=0.3)

plt.tight_layout()
plt.savefig('./ResultadosPY/4.png', dpi=300)
plt.show()


  # i[0] é o número de iterações, i[1] é a lista de erros, i[2] é o nome do método
#dessa forma podemos ver o comportamento exponencial do erro, e comparar melhor a convergencia dos métodos
# o x final nao e do interesse
# alguns dos metodos ultillizados podem retardar o tempo de cada metodo, uma vez que usamos os mesmo para todos faz com que na comparaçao isso nao seja um problema.
