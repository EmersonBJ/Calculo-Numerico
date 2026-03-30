# Question 5.
# Interpolando Dados Climáticos
# Objetivo: Explorar interpolação polinomial e o erro associado em dados reais.
# Descrição da Tarefa:
# 1. Considere dados de temperatura média em uma cidade em dias consecutivos (escolha uma cidade e procure no INMET).
# 2. Construa o polinômio interpolador usando os métodos:
#    - Lagrange,
#    - Newton,
#    - Gregory-Newton.
# 3. Compare os resultados e discuta a unicidade do polinômio interpolador.
# 4. Estime o erro de interpolação (teórico e prático) e analise como ele cresce com o grau do polinômio.
# Entrega: Código, gráficos com curvas interpoladas, tabela de erros e discussão crítica sobre as limitações 
# da interpolação polinomial.

# -----------------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt



# Referencias:
# [1] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.
