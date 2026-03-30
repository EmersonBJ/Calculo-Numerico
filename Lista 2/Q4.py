# ==============================================================================
# Question 4 - O Consumo de Energia em uma Rede Eletrica

# Objetivo: 
# Aplicar metodos diretos e iterativos para resolver sistemas lineares e 
# interpretar resultados no contexto de uma rede eletrica.
#
# Descricao da Tarefa:
# 1. Modele um sistema simples de rede eletrica (pelo menos 10 nos interconectados). 
#    As equacoes de balanco de energia/potencia podem ser representadas como um 
#    sistema linear A * x = b.

# 2. Por exemplo, considere a seguinte rede de 3 nos:
#
#       3x1 -  x2 +  x3 =  5
#      -2x1 + 4x2       =  6
#        x1 +  x2 + 5x3 = -4

#    Que pode ser escrita na forma matricial:
#
#        [ 3  -1   1 ]       [ x1 ]       [  5 ]
#    A = [-2   4   0 ]   x = [ x2 ]   b = [  6 ]     ->  A * x = b
#        [ 1   1   5 ]       [ x3 ]       [ -4 ]

# 3. Resolva o sistema pelos metodos:
#    - Cramer (para sistemas pequenos, 3x3 ou 4x4)
#    - Eliminacao de Gauss
#    - Decomposicao A = LU
#    - Jacobi e Gauss-Seidel (para sistemas maiores, simulando uma rede 10x10)

# 4. Compare numero de operacoes, tempo de execucao, estabilidade numerica e erros.

# Entrega: 
# Codigo, tabelas comparativas e relatorio critico discutindo qual metodo 
# e mais adequado em cada situacao.

import numpy as np
import time
A = np.array([[3, -1, 1], [-2, 4, 0], [1, 1, 5]])
x = np.array([1, 2, 3])
b = np.array([5, 6, -4])

def cramer(A, b):
    start = time.counter_time()
    det_A = np.linalg.det(A) # Determinante da matriz A
    det_x = np.linalg.det(np.column_stack((b, A[:, 1:]))) # Determinante da matriz com a primeira coluna substituida por b
    det_y = np.linalg.det(np.column_stack((A[:, 0], b, A[:, 2]))) # Determinante da matriz com a segunda coluna substituida por b
    det_z = np.linalg.det(np.column_stack((A[:, 0], A[:, 1], b))) # Determinante da matriz com a terceira coluna substituida por b
    end = time.counter_time()
    return det_x / det_A, det_y / det_A, det_z / det_A, (end - start)


# Para decomposiçao LU usamos o metodo de doolittle [1 - cap6]
def LU(A):
    start = time.perf_counter()
    n = len(A)
    
    # 1. Caracteristica do Algoritmo de Doolittle: Diagonal de L igual a 1
    L = np.eye(n) # Matriz identidade
    U = np.zeros((n, n)) # Matriz triangular superior

    for i in range(n): # Loop principal avanca na diagonal
        
        # 2. Calcula primeiro a linha de U (da diagonal para a direita)
        for j in range(i, n): 
            U[i, j] = A[i, j] - np.dot(L[i, :i], U[:i, j])
            # U[i, j] define os coeficientes da matriz triangular superior
            # Então, nós iteramos com o i representando as linhas e o j variando de i até n, olhando para a parte superior da matriz. 
            # Em seguida, para definir esses termos em U, pegamos o elemento correspondente da matriz A e subtraímos o produto escalar 
            # entre os elementos da linha de L (L[i, :i]- linha i e coluna de 0 até i-1) que estão diagonal inferior sem pivô (ignorando os pivôs que valem 1) e os elementos da coluna de U que estão acima da posição atual (U[:i, j]- linha de 0 até i-1 e coluna j).
        # 3. Calcula a coluna de L (apenas abaixo da diagonal)
        for j in range(i+1, n): 
            L[j, i] = (A[j, i] - np.dot(L[j, :i], U[:i, i])) / U[i, i]
            # L[j, i] define os multiplicadores da matriz triangular inferior
            # Iteramos com o j variando de i+1 até n, olhando para a parte inferior da matriz.
            # Em seguida, para definir esses termos em L, pegamos o elemento correspondente da matriz A e subtraímos o produto escalar 
            # entre os elementos da linha de L (L[j, :i]- linha j e coluna de 0 até i-1) que estão diagonal inferior sem pivô (ignorando os pivôs que valem 1) e os elementos da coluna de U que estão acima da posição atual (U[:i, i]- linha de 0 até i-1 e coluna i).
        
        # Por fim devemos resolver o sistema:
        # Onde y e x são vetores de tamanho n.
        y = np.linalg.solve(L, b) # funçao linalg resolve rapidamente o sistema para Ly = b  ou melhor, y = L^-1 * b
        x = np.linalg.solve(U, y) # funçao linalg resolve rapidamente o sistema para Ux = y ou melhor, x = U^-1 * y
        # Optamos pela funçao pronta NumPy, uma vez que a resoluçao do sistema nao foi o foco da aulas mas sim a decomposiçao LU.
    end = time.perf_counter()
    
    return x, y, (end - start)
    import numpy as np

#Eliminação de Gauss

import numpy as np

# Matrizes da imagem (Prof. Juliana)
A = np.array([
    [3, -1, 1],
    [-2, 4, 0],
    [1, 1, 5]
], dtype=float)

b = np.array([5, 6, -4], dtype=float)

def eliminacao_gauss_manual(A, b):
    n = len(b)
    Ab = np.column_stack((A, b)) # Matriz Aumentada

    # Escalonamento (Zerando abaixo da diagonal)
    for i in range(n):
        for k in range(i + 1, n):
            fator = Ab[k, i] / Ab[i, i]
            Ab[k, i:] -= fator * Ab[i, i:]

    # Substituição Retroativa
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (Ab[i, n] - np.dot(Ab[i, i+1:n], x[i+1:n])) / Ab[i, i]
    
    return x

# Resultado
solucao = eliminacao_gauss_manual(A, b)
print(f"Solução Exata: x1={solucao[0]:.2f}, x2={solucao[1]:.2f}, x3={solucao[2]:.2f}")

#Decomposição LU

import numpy as np

# Matrizes do exercício da Prof. Juliana
A = np.array([
    [3, -1, 1],
    [-2, 4, 0],
    [1, 1, 5]
], dtype=float)

b = np.array([5, 6, -4], dtype=float)

def resolucao_direta(A, b):
    # Usando o resolvedor padrão do Python (baseado em Gauss/LU)
    x = np.linalg.solve(A, b)
    
    print("Resolução do Sistema 3x3:")
    print(f"x1 = {x[0]:.4f}")
    print(f"x2 = {x[1]:.4f}")
    print(f"x3 = {x[2]:.4f}")
    return x

# Executa a conta
resolucao_direta(A, b)


#Jacobi

import numpy as np

# 1. Definição da Rede Elétrica (10 nós)
# Matriz A: Conexões da rede (Diagonal Dominante)
A = np.array([
    [10, -1,  1, -1,  1, -1,  1, -1,  1, -1], 
    [-1, 10, -1,  1, -1,  1, -1,  1, -1,  1], 
    [ 1, -1, 10, -1,  1, -1,  1, -1,  1, -1], 
    [-1,  1, -1, 10, -1,  1, -1,  1, -1,  1], 
    [ 1, -1,  1, -1, 10, -1,  1, -1,  1, -1], 
    [-1,  1, -1,  1, -1, 10, -1,  1, -1,  1], 
    [ 1, -1,  1, -1,  1, -1, 10, -1,  1, -1], 
    [-1,  1, -1,  1, -1,  1, -1, 10, -1,  1], 
    [ 1, -1,  1, -1,  1, -1,  1, -1, 10, -1], 
    [-1,  1, -1,  1, -1,  1, -1,  1, -1, 10]
], dtype=float)

# Vetor b: Cargas/Fontes de energia nos nós
b = np.array([5, 3, 7, 2, 8, 4, 6, 1, 9, 0], dtype=float)

def metodo_jacobi(A, b, tolerancia=1e-4, max_iter=100):
    n = len(b)
    x = np.zeros(n)  # Chute inicial (todos os nós em 0)
    
    print(f"{'Volta':<10} | {'Erro (Diferença)':<15}")
    print("-" * 30)

    for k in range(max_iter):
        x_novo = np.zeros(n)
        
        for i in range(n):
            # Soma de todos os elementos exceto a diagonal
            soma_outros = b[i] - (np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x[i+1:]))
            x_novo[i] = soma_outros / A[i, i]
        
        # Cálculo do erro absoluto (Norma Infinita)
        erro = np.linalg.norm(x_novo - x, ord=np.inf)
        print(f"{k+1:<10} | {erro:.6f}")

        if erro < tolerancia:
            return x_novo, k + 1
        
        x = x_novo.copy()
        
    return x, max_iter

# Execução do Algoritmo
solucao, total_voltas = metodo_jacobi(A, b)

print("-" * 30)
print(f"\nSucesso! Convergência em {total_voltas} iterações.")
print("Energia calculada em cada nó (x):")
for i, valor in enumerate(solucao):
    print(f"Nó {i+1}: {valor:.4f}")

#Gauss-Seidel

import numpy as np

# 1. Configuração da Rede 10x10 (Matriz da sua imagem)
A = np.array([
    [10, -1,  1, -1,  1, -1,  1, -1,  1, -1], 
    [-1, 10, -1,  1, -1,  1, -1,  1, -1,  1], 
    [ 1, -1, 10, -1,  1, -1,  1, -1,  1, -1], 
    [-1,  1, -1, 10, -1,  1, -1,  1, -1,  1], 
    [ 1, -1,  1, -1, 10, -1,  1, -1,  1, -1], 
    [-1,  1, -1,  1, -1, 10, -1,  1, -1,  1], 
    [ 1, -1,  1, -1,  1, -1, 10, -1,  1, -1], 
    [-1,  1, -1,  1, -1,  1, -1, 10, -1,  1], 
    [ 1, -1,  1, -1,  1, -1,  1, -1, 10, -1], 
    [-1,  1, -1,  1, -1,  1, -1,  1, -1, 10]
], dtype=float)

b = np.array([5, 3, 7, 2, 8, 4, 6, 1, 9, 0], dtype=float)

def gauss_seidel(A, b, tol=1e-4, max_iter=100):
    n = len(b)
    x = np.zeros(n)  # Chute inicial (Nós em zero)
    
    for k in range(max_iter):
        x_anterior = x.copy()
        
        for i in range(n):
            # A diferença aqui: usamos o 'x' atualizado na mesma iteração
            soma_atualizados = np.dot(A[i, :i], x[:i])
            soma_antigos = np.dot(A[i, i+1:], x_anterior[i+1:])
            
            x[i] = (b[i] - soma_atualizados - soma_antigos) / A[i, i]
        
        # Critério de Parada (Diferença entre voltas)
        if np.linalg.norm(x - x_anterior, ord=np.inf) < tol:
            return x, k + 1
            
    return x, max_iter

# Execução
solucao, total_voltas = gauss_seidel(A, b)

print(f"Gauss-Seidel: Convergência em {total_voltas} iterações.")
print("Resultados finais para os 10 nós:")
print(np.round(solucao, 4))


# Referencias:
# [1] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.
