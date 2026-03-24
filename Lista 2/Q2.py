# Question 2.
# Descreva, fazendo um passo-a-passo explicativo (pode conter um pseudo-código, fluxograma, etc), como 
# resolver sistemas de equações lineares usando os métodos diretos: 
# (i) de Cramer
# (ii) eliminação de Gauss 
# (iii) decomposição A=LU.

# -----------------------------------------------------------------------------------------
# Metodos diretos acham a solucao exata (ignorando erro de maquina) num numero finito de passos
# Forma geral: Ax = b
# =========================================================================================

print("METODO 1: REGRA DE CRAMER")
print("-" * 50)
"""
Baseado em determinantes. Bom pra matrizes pequenas, pesado demais para matrizes grandes.
Passos:
1. Calcular o determinante da matriz original A (det_A). Se der 0, o sistema nao tem solucao unica.
2. Para achar cada incognita 'i', substituir a coluna 'i' de A pelos valores de 'b' (formando Ai).
3. Calcular det_Ai.
4. O valor da incognita é: x_i = det_Ai / det_A.
"""

# [1] Cap 6.1 - Sistemas Lineares e Eliminacao de Gauss
print("\nMETODO 2: ELIMINACAO DE GAUSS")
print("-" * 50)
"""
Processo de escalonamento para zerar tudo abaixo da diagonal principal.
Passos:
1. Monta a matriz aumentada [A|b].
2. Forward (Eliminacao): pega a diagonal (pivo) e usa pra zerar as linhas de baixo. 
   O multiplicador = A[linha][coluna_do_pivo] / Pivo. Subtrai a linha ajustada.
3. Repete o passo 2 ate formar uma matriz triangular superior.
4. Backward (Substituicao): A ultima equacao fica trivial (ex: 2z = 4 -> z = 2). 
   Achado o ultimo, volta substituindo nas esquacoes de cima pra achar as outras variaveis.
"""

# [1] Cap 6.5 - Fatorizacao de Matrizes
print("\nMETODO 3: DECOMPOSICAO A=LU")
print("-" * 50)
"""
Separa a matriz A em Lower (Triangulo Inferior L) e Upper (Triangulo Superior U). Excelente pra 
reaproveitar a matriz quando so o vetor 'b' muda.
Passos:
1. A matriz U eh o exato resultado da eliminacao de Gauss (passo 2 do metodo anterior).
2. A matriz L tem diagonal unitaria (só "1") e abaixo dela a gente preenche com os "multiplicadores" 
   que foram usados no Gauss pra zerar as variaveis.
3. O sistema A*x = b é trocado para L*y = b.
4. Resolve L*y = b por substituicao progressiva (de cima pra baixo) achando 'y'.
5. Com 'y' e 'U' na mao, calcula U*x = y por substituicao regressiva (de baixo pra cima) e acha 'x'.
"""
