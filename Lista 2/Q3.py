# Question 3.
# Descreva, fazendo um passo-a-passo explicativo (pode conter um pseudo-código, fluxograma, etc), como 
# resolver sistemas de equações lineares usando os métodos iterativos: 
# (i) Jacobi 
# (ii) Gauss-Seidel.
# Norma ||B|| < 1.0 implica em um sistema convergente, extritamente diagonalmente dominante, criterio de convergencia de Sassenfeld.

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
