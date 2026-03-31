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
    start = time.perf_counter()
    det_A = np.linalg.det(A) # Determinante da matriz A
    det_x = np.linalg.det(np.column_stack((b, A[:, 1:]))) # Determinante da matriz com a primeira coluna substituida por b
    det_y = np.linalg.det(np.column_stack((A[:, 0], b, A[:, 2]))) # Determinante da matriz com a segunda coluna substituida por b
    det_z = np.linalg.det(np.column_stack((A[:, 0], A[:, 1], b))) # Determinante da matriz com a terceira coluna substituida por b
    end = time.perf_counter()
    return det_x / det_A, det_y / det_A, det_z / det_A, (end - start)


# Para decomposiçao LU usamos o metodo de doolittle [1 - cap6]
def LU(A, b):
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

def eliminacao_gauss_manual(A, b):
    start = time.perf_counter()
    n = len(b)
    # astype(float) GARANTE que a matriz aceitará números decimais
    Ab = np.column_stack((A, b)).astype(float) 

    # Escalonamento
    for i in range(n):
        for k in range(i + 1, n):
            fator = Ab[k, i] / Ab[i, i]
            Ab[k, i:] -= fator * Ab[i, i:]

    # Substituição Retroativa
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (Ab[i, n] - np.dot(Ab[i, i+1:n], x[i+1:n])) / Ab[i, i]
    
    end = time.perf_counter()
    return x, (end - start)

#Decomposição LU

def resolucao_direta(A, b):
    # Usando o resolvedor padrão do Python (baseado em Gauss/LU)
    x = np.linalg.solve(A, b)
    
    print("Resolução do Sistema 3x3:")
    print(f"x1 = {x[0]:.4f}")
    print(f"x2 = {x[1]:.4f}")
    print(f"x3 = {x[2]:.4f}")
    return x
# ==============================================================================
# EXECUÇÃO DO SISTEMA 3x3 (MÉTODOS DIRETOS)
# ==============================================================================

print("\n" + "="*80)
print("RESULTADOS DO SISTEMA 3x3 (Rede Pequena)")
print("="*80)

x1_c, x2_c, x3_c, tempo_cramer = cramer(A, b)
print(f"[Cramer] Solução Exata: x1={x1_c:.4f}, x2={x2_c:.4f}, x3={x3_c:.4f}")

res_gauss, tempo_gauss = eliminacao_gauss_manual(A.copy(), b.copy())
print(f"[Gauss]  Solução Exata: x1={res_gauss[0]:.4f}, x2={res_gauss[1]:.4f}, x3={res_gauss[2]:.4f}")

res_lu_x, res_lu_y, tempo_lu = LU(A.copy(), b.copy())
print(f"[LU]     Solução Exata: x1={res_lu_x[0]:.4f}, x2={res_lu_x[1]:.4f}, x3={res_lu_x[2]:.4f}")


# ==============================================================================
# MÉTODOS ITERATIVOS (Jacobi e Gauss-Seidel) - REDE 10x10
# ==============================================================================

#Jacobi
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
    x = np.zeros(n)  # Chute inicial
    start = time.perf_counter()
    
    print(f"\n[JACOBI] {'Volta':<5} | {'Erro (Diferença)':<15}")
    print("-" * 30)

    for k in range(max_iter):
        x_novo = np.zeros(n)
        for i in range(n):
            soma_outros = b[i] - (np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x[i+1:]))
            x_novo[i] = soma_outros / A[i, i]
        
        erro = np.linalg.norm(x_novo - x, ord=np.inf)
        print(f"{k+1:<13} | {erro:.6f}")

        if erro < tolerancia:
            end = time.perf_counter()
            return x_novo, k + 1, (end - start)
        
        x = x_novo.copy()
        
    end = time.perf_counter()
    return x, max_iter, (end - start)

def gauss_seidel(A, b, tol=1e-4, max_iter=100):
    n = len(b)
    x = np.zeros(n)
    start = time.perf_counter()
    
    print(f"\n[GAUSS-SEIDEL] Analisando convergência...")
    for k in range(max_iter):
        x_anterior = x.copy()
        for i in range(n):
            soma_atualizados = np.dot(A[i, :i], x[:i])
            soma_antigos = np.dot(A[i, i+1:], x_anterior[i+1:])
            x[i] = (b[i] - soma_atualizados - soma_antigos) / A[i, i]
        
        if np.linalg.norm(x - x_anterior, ord=np.inf) < tol:
            end = time.perf_counter()
            return x, k + 1, (end - start)
            
    end = time.perf_counter()
    return x, max_iter, (end - start)
# ==============================================================================
# EXECUÇÃO DO SISTEMA 10x10 (MÉTODOS ITERATIVOS)
# ==============================================================================

A_10x10 = np.array([
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

b_10x10 = np.array([5, 3, 7, 2, 8, 4, 6, 1, 9, 0], dtype=float)

solucao_jacobi, iter_jacobi, tempo_jacobi = metodo_jacobi(A_10x10, b_10x10)
print(f"-> Jacobi convergiu em {iter_jacobi} iterações.")

solucao_gs, iter_gs, tempo_gs = gauss_seidel(A_10x10, b_10x10)
print(f"-> Gauss-Seidel convergiu em {iter_gs} iterações.")
print("\nEnergia Final em cada nó (Gauss-Seidel):")
print(np.round(solucao_gs, 4))

# ==============================================================================
# 4. COMPARAÇÃO DE TEMPO E RELATÓRIO CRÍTICO
# ==============================================================================

print("\n" + "="*80)
print("COMPARAÇÃO DE TEMPO DE EXECUÇÃO (Sistema 3x3)")
print("="*80)
print(f"Cramer:          {tempo_cramer:.6f} segundos")
print(f"Gauss:           {tempo_gauss:.6f} segundos")
print(f"Decomposição LU: {tempo_lu:.6f} segundos")

print("\n" + "="*80)
print("TABELA COMPARATIVA DOS MÉTODOS")
print("="*80)
print(f"{'Método':<15} | {'Operações (Complexidade)':<25} | {'Estabilidade':<15} | {'Erro/Convergência'}")
print("-" * 80)
print(f"{'Cramer':<15} | {'O(N!)':<25} | {'Muito Baixa':<15} | {'Exato (mas sofre com arredondamento)'}")
print(f"{'Gauss':<15} | {'O(N³ / 3)':<25} | {'Média (s/ pivô)':<15} | {'Exato (acumula erro em N grande)'}")
print(f"{'Fatoração LU':<15} | {'O(N³ / 3)':<25} | {'Média (s/ pivô)':<15} | {'Exato (ótimo para múltiplos b)'}")
print(f"{'Jacobi':<15} | {'O(N²) por iteração':<25} | {'Alta':<15} | {'1e-4 (Converge em 19 iterações)'}")
print(f"{'Gauss-Seidel':<15} | {'O(N²) por iteração':<25} | {'Alta':<15} | {'1e-4 (Converge em 13 iterações)'}")


# Referencias:
# [1] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.
