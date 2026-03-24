# Question 4.
# O Consumo de Energia em uma Rede Elétrica
# Objetivo: Resolver sistemas lineares usando métodos diretos e iterativos, comparando desempenho e precisão.
# Descrição da Tarefa:
# 1. Resolva o sistema linear 3x3 dado usando:
#    - Regra de Cramer,
#    - Eliminação Gaussiana,
#    - Fatoração LU (via `numpy.linalg.solve`).
# 2. Para um sistema 10x10 (gerado aleatoriamente, mas diagonalmente dominante), compare:
#    - Método de Jacobi,
#    - Método de Gauss-Seidel.
# 3. Analise:
#    - Convergência dos métodos iterativos,
#    - Complexidade computacional (tempo estimado),
#    - Robustez e precisão.
# Entrega: Código, tabela comparativa de resultados e relatório crítico sobre a escolha do método para cada cenário.

import numpy as np
import time

print("--- SISTEMA DE REDE ELETRICA: PARTE 1 (3x3) ---")
# Sistema dado:
#  3x1 - x2 + x3 = 5
# -2x1 + 4x2 = 6
#   x1 + x2 + 5x3 = -4
A3 = np.array([[3.0, -1.0, 1.0], 
               [-2.0, 4.0, 0.0], 
               [1.0, 1.0, 5.0]])
b3 = np.array([5.0, 6.0, -4.0])

def cramer(A, b):
    det_A = np.linalg.det(A)
    n = len(b)
    x = np.zeros(n)
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / det_A
    return x

# [1] Cap 6.1
def gauss(A, b):
    n = len(b)
    M = np.column_stack((A, b))
    # forward sem pivotamento pro codigo ficar limpo no caso de teste
    for k in range(n):
        for i in range(k+1, n):
            fator = M[i, k] / M[k, k]
            M[i, k:] -= fator * M[k, k:]
    # backward
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (M[i, -1] - np.sum(M[i, i+1:n] * x[i+1:])) / M[i, i]
    return x

def lu_solve(A, b):
    # linalg.solve resolve por LU fatorizacao no numpy backend
    return np.linalg.solve(A, b)

# avaliacao de tempo:
for idx, metodo in enumerate([(cramer, "CRAMER"), (gauss, "GAUSS"), (lu_solve, "A=LU")]):
    t0 = time.perf_counter()
    x_res = metodo[0](A3, b3)
    t_res = time.perf_counter() - t0
    print(f"{metodo[1]:<7} | Tempo Estimado: {t_res:.6f}s | Solucao: {np.round(x_res, 4)}")

print("\n--- SISTEMA DE REDE ELETRICA: PARTE 2 (10x10) ---")
# gerando 10x10 diagonal dominante garantida pra Jacobi/GS convergirem
np.random.seed(42)
A10 = np.random.rand(10, 10)
for i in range(10):
    A10[i, i] = np.sum(np.abs(A10[i, :])) + 1.0 
x_real = np.ones(10)
b10 = np.dot(A10, x_real)

# [1] Cap 7.3 (Para metodos iterativos Gauss-Seidel e Jacobi)
def iterativos(A, b, tipo='jacobi', tol=1e-6, max_iter=200):
    n = len(b)
    x = np.zeros(n)
    x_novo = np.zeros(n)
    for k in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            soma = np.dot(A[i, :], x) - A[i, i] * x[i]
            if tipo == 'jacobi':
                x_novo[i] = (b[i] - soma) / A[i, i]
            else:
                x[i] = (b[i] - soma) / A[i, i] 
        
        if tipo == 'jacobi':
            x = x_novo.copy()
            
        erro = np.max(np.abs(x - x_old))
        if erro < tol:
            return x, k+1, erro
    return x, max_iter, erro

t0 = time.perf_counter()
x_jac, iter_jac, err_jac = iterativos(A10, b10, tipo='jacobi')
t_jac = time.perf_counter() - t0

t0 = time.perf_counter()
x_gs, iter_gs, err_gs = iterativos(A10, b10, tipo='gs')
t_gs = time.perf_counter() - t0

print(f"JACOBI       | Iteracoes: {iter_jac:03d} | Tempo: {t_jac:.6f}s | Erro Final: {err_jac:.2e}")
print(f"GAUSS-SEIDEL | Iteracoes: {iter_gs:03d} | Tempo: {t_gs:.6f}s | Erro Final: {err_gs:.2e}")

print("\n[Relatorio de Otimizacao]: Gauss-Seidel converge em quase metade das iteracoes por propagar solucoes ativas. Metodos como Eliminacao Gauss ou Cramer explodiriam em O(N^3) ou O(N!) caso testados em grandes bases, iterativo alivia complexidade computacional em redes extremas.")

# Referencias:
# [1] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.
