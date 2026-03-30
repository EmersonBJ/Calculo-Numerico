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


# Jacobi
A = np.array([
    [10, -1, 1, -1, 1, -1, 1, -1, 1, -1], 
    [-1, 10, -1, 1, -1, 1, -1, 1, -1, 1], 
    [1, -1, 10, -1, 1, -1, 1, -1, 1, -1], 
    [-1, 1, -1, 10, -1, 1, -1, 1, -1, 1], 
    [1, -1, 1, -1, 10, -1, 1, -1, 1, -1], 
    [-1, 1, -1, 1, -1, 10, -1, 1, -1, 1], 
    [1, -1, 1, -1, 1, -1, 10, -1, 1, -1], 
    [-1, 1, -1, 1, -1, 1, -1, 10, -1, 1], 
    [1, -1, 1, -1, 1, -1, 1, -1, 10, -1], 
    [-1, 1, -1, 1, -1, 1, -1, 1, -1, 10]
], dtype=float)

b = np.array([5, 3, 7, 2, 8, 4, 6, 1, 9, 0], dtype=float)

# chute inicial passado para a funcao (sera sobrescrito por b* dentro dela)

t = 0.0001 # Tolerancia
it = 100 # Numero maximo de iteracoes

def Jacobi(A, b, x, t, it):
    # Analise dos criterios de convergencia
    # Norma ||B|| < 1 implica convergencia (criterio do Jacobi)
    # Obs: criterio de Sassenfeld e variante especifica para Gauss-Seidel, nao para Jacobi

    # Ax = b -> x^(k+1) = B*x^(k) + g
    # Supondo det D != 0
    # A = L + D + R, sendo L triangular inferior, D diagonal, R triangular superior
    L = np.tril(A, -1)   # estritamente abaixo da diagonal (k=-1 exclui diagonal)
    D = np.diag(np.diag(A))  # apenas a diagonal
    R = np.triu(A,  1)   # estritamente acima da diagonal (k=1 exclui diagonal)
    # Onde:
    # lij = aij se i > j ou 0 se i <= j  (triangulo inferior sem pivo)
    # dij = aij se i = j ou 0 se i != j  (diagonal principal)
    # rij = aij se i < j ou 0 se i >= j  (triangulo superior sem pivo)
    # (L + D + R)x = b
    # Dx = b - (L + R)x
    # x^(k+1) = D^-1 * (b - (L+R)*x^(k))

    # Normalizando por D: definimos B = -D^-1*(L+R) e g = D^-1*b
    # x^(k+1) = B*x^(k) + g
    D_inv = np.diag(1.0 / np.diag(A))   # D^-1: cada 1/a_ii na diagonal
    B = -np.dot(D_inv, L + R)            # matriz de iteracao do Jacobi
    g = np.dot(D_inv, b)                 # g = D^-1*b = b* (vetor normalizado)

    # chute inicial: x^(0) = b* conforme proposto pela professora em sala
    # (equivalente a uma iteracao a partir do zero, mas mais rapido na pratica)
    x = g.copy()

    # verificacao: se ||B||_inf < 1, o metodo GARANTE convergencia
    norma_B = np.linalg.norm(B, ord=np.inf)
    print(f"Verificacao de convergencia: ||B||_inf = {norma_B:.4f} ", end="")
    if norma_B < 1:
        print("< 1 -> CONVERGENTE")
    else:
        print(">= 1 -> PODE NAO CONVERGIR")

    start = time.perf_counter()

    # loop de ponto fixo: x^(k+1) = B*x^(k) + g
    for iteracao in range(it):
        x_novo = np.dot(B, x) + g

        # criterio de parada: norma infinita da correcao
        erro = np.linalg.norm(x_novo - x, ord=np.inf)
        if erro < t:
            end = time.perf_counter()
            print(f"Convergiu em {iteracao+1} iteracoes. Tempo: {end - start:.6f}s")
            return x_novo

        x = x_novo  # atualiza APOS calcular todos os x_novo da rodada

    end = time.perf_counter()
    print(f"Nao convergiu no limite de {it} iteracoes. Tempo: {end - start:.6f}s")
    return x

solucao = Jacobi(A, b, x, t, it)

print("\n--- Solucao do Sistema 10x10 ---")
for i, valor in enumerate(solucao):
    print(f"x{i+1} = {valor:.4f}")

# Referencias:
# [1] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.
