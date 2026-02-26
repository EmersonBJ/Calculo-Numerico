# ==============================================================================
# Question 5. Um Problema Real: O Pêndulo e a Busca de Ângulos
# ==============================================================================
# Objetivo: Usar métodos numéricos para resolver um problema físico real.
#
# Descrição da Tarefa:
# 1. Considere a equação transcendental do período aproximado de um pêndulo simples:
#    f(theta) = math.sin(theta) - (T / (2 * math.pi)) * math.sqrt(g / L) = 0
#    onde T é o período medido, L o comprimento e g a gravidade.
# 2. Dado um período T observado, estime o ângulo inicial theta.
# 3. Resolva o problema usando: bisseção, Newton-Raphson e secante.
# 4. Analise o efeito de aproximações numéricas (arredondamento) no resultado.
#
# Entrega: Código, gráficos mostrando a evolução das aproximações e discussão do modelo.

import math
import time
import numpy as np

#Var fixo
g = 9.81
L = 1
T = 2.0 #Período observado arbitrário.

def f(theta, T, g, L, mode = "float64"):
    if mode == "float32":
        return np.float32(math.sin(theta) - (T / (2 * math.pi)) * math.sqrt(g / L))
    elif mode == "trunc":
        return round(math.sin(theta) - (T / (2 * math.pi)) * math.sqrt(g / L), 5)
    return math.sin(theta) - (T / (2 * math.pi)) * math.sqrt(g / L)

def df(theta, T, g, L, mode = "float64"): 
    if mode == "float32":
        return np.float32(math.cos(theta))
    elif mode == "trunc":
        return round(math.cos(theta))
    return math.cos(theta) 

Raizes = math.asin((T / (2 * math.pi)) * math.sqrt(g / L)) #[1.49301 + k*math.pi, 1.64858 + k*math.pi] 

def Bissecao(a, b, t, T, L, mode = "float64"):
    name = f"Bisseção {mode}"
    it = 0
    e = [] 
    start_time = time.perf_counter()

    while abs(b - a) > t and it < 100: 
        c = (a + b) / 2
        e.append(abs(c - Raizes)) 

        if f(c, T, g, L) == 0:
            break
        elif f(a, T, g, L) * f(c, T, g, L) < 0:
            b = c
        else:
            a = c
        it += 1
    theta = c
    tempo = time.perf_counter() - start_time
    return theta, it, e, name, tempo


def Newton(theta, t, T, L, mode = "float64"): # x, tolerancia, periodo, comprimento, modo de arredondamento
    name = f"Newton-Raphson {mode}"
    it = 0
    e = [] 
    start_time = time.perf_counter()

    while it < 100: 
        if df(theta[it], T, g, L, mode) == 0: break 

        if mode == "float32":
            x_novo = np.float32(theta[it] - f(theta[it], T, g, L, mode)/df(theta[it], T, g, L, mode))
            theta.append(np.float32(x_novo))
            
        elif mode == "trunc":
            x_novo = np.trunc((theta[it] - f(theta[it], T, g, L, mode)/df(theta[it], T, g, L, mode))*10e3)/10e3
            theta.append(np.trunc(x_novo*10e3)/10e3)

        elif mode == "float64":
            x_novo = theta[it] - f(theta[it], T, g, L, mode)/df(theta[it], T, g, L, mode)
            theta.append(x_novo)

        it += 1
        e.append(abs(theta[it] - Raizes))

        if abs(theta[it] - theta[it-1]) < t:
            break
    tempo = time.perf_counter() - start_time
    return theta[-1], it, e, name, tempo


def secante(theta, t, T, L, mode = "float64"):
    name = f"Secante {mode}"
    it = 1 
    e = [] 
    start_time = time.perf_counter()

    while it < 100: 
        if f(theta[it], T, g, L, mode) - f(theta[it-1], T, g, L, mode) == 0: break 

        if mode == "float32":
            novo_x = np.float32(theta[it] - (((theta[it] - theta[it-1]) * f(theta[it], T, g, L, mode)) / (f(theta[it], T, g, L, mode) - f(theta[it-1], T, g, L, mode))))
            theta.append(np.float32(novo_x))

        elif mode == "trunc":
            novo_x = np.trunc((theta[it] - (((theta[it] - theta[it-1]) * f(theta[it], T, g, L, mode)) / (f(theta[it], T, g, L, mode) - f(theta[it-1], T, g, L, mode))))*10e3)/10e3
            theta.append(np.trunc(novo_x*10e3)/10e3)

        elif mode == "float64":        
            novo_x = theta[it] - (((theta[it] - theta[it-1]) * f(theta[it], T, g, L, mode)) / (f(theta[it], T, g, L, mode) - f(theta[it-1], T, g, L, mode)))
            theta.append(novo_x)
        
        it += 1
        e.append(abs(theta[it] - Raizes))
        

        if abs(theta[it] - theta[it-1]) < t:
            break
    
    tempo = time.perf_counter() - start_time
    return theta[-1], it, e, name, tempo


R = [Bissecao(0, math.pi/2, 1e-5, T, L,), Newton([0.5], 1e-5, T, L), secante([0.5, 0.6], 1e-5, T, L), Bissecao(0, math.pi/2, 1e-5, T, L, mode="float32"), Newton([0.5], 1e-5, T, L, mode="float32"), secante([0.5, 0.6], 1e-5, T, L, mode="float32"), Bissecao(0, math.pi/2, 1e-5, T, L, mode="trunc"), Newton([0.5], 1e-5, T, L, mode="trunc"), secante([0.5, 0.6], 1e-5, T, L, mode="trunc")]
R.sort(key=lambda x: x[1]) # Ordena pelo número de iterações [1] do vetor R
# [x][y] x = método(Bissecao, Newton, Secante), y = (theta final, iterações, erros, nome do método, tempo)
import pandas as pd


data_struct = {
    'Método': [R[0][3], R[1][3], R[2][3], R[3][3], R[4][3], R[5][3], R[6][3], R[7][3], R[8][3]],    
    'Ângulo (rad)': [R[0][0], R[1][0], R[2][0], R[3][0], R[4][0], R[5][0], R[6][0], R[7][0], R[8][0]],
    'Iterações': [R[0][1], R[1][1], R[2][1], R[3][1], R[4][1], R[5][1], R[6][1], R[7][1], R[8][1]],
    'Tempo (s)': [R[0][4], R[1][4], R[2][4], R[3][4], R[4][4], R[5][4], R[6][4], R[7][4], R[8][4]]
}
df = pd.DataFrame(data_struct)
print(df)
df.to_csv('./ResultadosPY/Q5.csv', index=False)

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 7))

# 1. Definimos uma cor fixa para cada método (independente da precisão)
cor_metodo = {
    'Bisseção': '#3498db',        # Azul
    'Newton-Raphson': '#2ecc71',  # Verde
    'Secante': '#e74c3c'          # Vermelho
}

# 2. Definimos um estilo de linha e marcador para cada tipo de precisão
estilo_precisao = {
    'float64': {'ls': '-', 'marker': 'o'},   # Linha contínua e Bolinha
    'float32': {'ls': '--', 'marker': 's'},  # Linha tracejada e Quadrado (Square)
    'trunc': {'ls': ':', 'marker': '^'}      # Linha pontilhada e Triângulo
}

for i in R:
    nome_completo = i[3]
    erros = i[2]
    
    # Separa a string do nome. Ex: "Bisseção float64" vira ["Bisseção", "float64"]
    partes = nome_completo.rsplit(' ', 1)
    nome_base = partes[0]
    precisao = partes[1]
    
    # Busca a cor e o estilo nos nossos dicionários
    c = cor_metodo.get(nome_base, '#000000')
    estilo = estilo_precisao.get(precisao, {'ls': '-', 'marker': 'x'})

    plt.plot(
        range(1, len(erros) + 1), 
        erros, 
        color=c, 
        linestyle=estilo['ls'], 
        marker=estilo['marker'], 
        linewidth=2, 
        label=nome_completo,
        alpha=0.8 # Deixa a linha levemente transparente para facilitar a leitura caso se cruzem
    )

plt.yscale('log') 
plt.xlabel('Número de Iterações', fontsize=11)
plt.ylabel('Erro Absoluto |theta - raiz_exata|', fontsize=11)
plt.title('Busca do Ângulo: Efeito do Arredondamento e Truncamento', fontsize=14)

# Como temos 9 linhas, colocamos a legenda do lado de fora do gráfico para não poluir
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.grid(True, which="both", ls="--", alpha=0.6)
plt.tight_layout() # Ajusta a margem automaticamente para a legenda não ficar cortada
plt.show()
plt.savefig('./ResultadosPY/5.png', dpi=300)