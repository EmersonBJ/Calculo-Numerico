# Question 3.
# Descreva, fazendo um passo-a-passo explicativo (pode conter um pseudo-código, fluxograma, etc), como 
# resolver sistemas de equações lineares usando os métodos iterativos: 
# (i) Jacobi 
# (ii) Gauss-Seidel.
# Norma ||B|| < 1.0 implica em um sistema conbergente, extritamente diagonalmente dominante, criterio de convergencia de Sassenfeld.

import math
import time

print("METODO 1: JACOBI")
print("-" * 50)
'''
Passos:
1. Isolar cada variavel na sua respectiva equacao da diagonal principal.
2. Definir um chute inicial x0 para todas as incognitas (normalmente zeros).
3. Usar os valores da iteracao k para calcular as aproximacoes da iteracao k+1.
4. Regra: iterar todas as variaveis usando APENAS os velhos valores da rodada k.
5. So atualizar o vetor de solucoes no final da iteracao k inteira.
6. Repetir ate a diferenca absoluta alcancar a tolerancia.
'''

print("\nMETODO 2: GAUSS-SEIDEL")
print("-" * 50)
'''
Passos: Identicos ao Jacobi, exceto pelo passo 4 e 5.
Regra: ao calcular o valor da variavel k+1, atualizar diretamente no vetor principal. 
Isso faz com que as proximas variaveis da mesma rodada ja utilizem a melhor estimativa 
recente, o que acelera drasticamente a convergencia.
'''

# [1] Cap 7.3 - Tecnicas Iterativas para Solucao de Sistemas Lineares (Jacobi)
def jacobi(A, b, tol=1e-5, max_iter=100):
    n = len(A)
    x = [0.0] * n  # vetor solucao atual
    x_novo = [0.0] * n # vetor auxiliar 
    
    for k in range(max_iter):
        for i in range(n):
            # calcula usando apenas os dados da iteracao anterior
            x_novo[i] = (b[i] - sum(A[i][j] * x[j] for j in range(n) if i != j)) / A[i][i]
            
        # avalia o erro / parada
        if max(abs(x_novo[i] - x[i]) for i in range(n)) < tol:
            return x_novo, k+1
            
        # só atualiza quando a iteracao completa acabar
        x = x_novo.copy()
        
    return x, max_iter

# [1] Cap 7.3 - Tecnicas Iterativas (Gauss-Seidel)
def gauss_seidel(A, b, tol=1e-5, max_iter=100):
    n = len(A)
    x = [0.0] * n 
    
    for k in range(max_iter):
        x_velho = x.copy()
        for i in range(n):
            # ja atualiza e usa na hora o proximo x[j] 
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(n) if i != j)) / A[i][i] 
            
        if max(abs(x[i] - x_velho[i]) for i in range(n)) < tol:
            return x, k+1
            
    return x, max_iter

if __name__ == "__main__":
    print("\n--- TESTES DE CONVERGENCIA ---")
    
    # teste convergente: diagonal estritamente dominante (10 > 2+1)
    A_boa = [[10, 2, 1], [1, 5, 1], [2, 3, 10]]
    b_boa = [7, -8, 6]
    
    print("\nSistema Convergente (Diagonal Dominante):")
    res_j, iter_j = jacobi(A_boa, b_boa)
    res_gs, iter_gs = gauss_seidel(A_boa, b_boa)
    
    print(f"JACOBI       | Iters: {iter_j:02d} | Resultado: {[round(v, 4) for v in res_j]}")
    print(f"GAUSS-SEIDEL | Iters: {iter_gs:02d} | Resultado: {[round(v, 4) for v in res_gs]}")
    
    # teste divergente: matriz com diagonal nao dominante explodira os valores
    A_ruim = [[1, 5, 1], [10, 2, 1], [2, 3, 1]]
    b_ruim = [-8, 7, 6]
    
    print("\nSistema Divergente (Nao atende criterio Sassenfeld):")
    res_ruim, _ = gauss_seidel(A_ruim, b_ruim, max_iter=20)
    print(f"GAUSS-SEIDEL | Iters: 20 (Max) | Falha! Valores divergem -> {[round(v, 2) for v in res_ruim]}")

# Referencias:
# [1] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.
