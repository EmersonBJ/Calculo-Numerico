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

# =========================
# DADOS
# =========================
x = np.array([1,2,3,4,5,6,7,8], dtype=float)
y = np.array([25.8,24.3,24.6,20.2,17.6,19.6,22.2,23.3], dtype=float)

# =========================
# 1. LAGRANGE
# =========================
def lagrange(x, y, xp):
    n = len(x)
    yp = 0
    for i in range(n):
        L = 1
        for j in range(n):
            if i != j:
                L *= (xp - x[j]) / (x[i] - x[j])
        yp += y[i] * L
    return yp

# =========================
# 2. NEWTON (Diferenças Divididas)
# =========================
def newton_coef(x, y):
    n = len(x)
    coef = np.copy(y)
    for j in range(1, n):
        coef[j:n] = (coef[j:n] - coef[j-1:n-1]) / (x[j:n] - x[0:n-j])
    return coef

def newton_eval(coef, x_data, xp):
    n = len(coef)
    yp = coef[n-1]
    for k in range(1, n):
        yp = coef[n-k-1] + (xp - x_data[n-k-1]) * yp
    return yp

coef_newton = newton_coef(x, y)

# =========================
# 3. GREGORY-NEWTON (Diferenças Finitas)
# =========================
def forward_diff_table(y):
    n = len(y)
    table = np.zeros((n, n))
    table[:,0] = y
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = table[i+1][j-1] - table[i][j-1]
    return table

def gregory_newton(x, y, xp):
    h = x[1] - x[0]
    s = (xp - x[0]) / h
    table = forward_diff_table(y)
    
    yp = y[0]
    fact = 1
    s_term = 1
    
    for i in range(1, len(y)):
        s_term *= (s - (i-1))
        fact *= i
        yp += (s_term * table[0][i]) / fact
        
    return yp

# =========================
# GERAÇÃO DOS PONTOS
# =========================
xp = np.linspace(1, 8, 200)

yl = np.array([lagrange(x, y, xi) for xi in xp])
yn = np.array([newton_eval(coef_newton, x, xi) for xi in xp])
yg = np.array([gregory_newton(x, y, xi) for xi in xp])

# =========================
# GRÁFICO
# =========================
plt.figure()
plt.scatter(x, y, label="Dados reais")
plt.plot(xp, yl, linestyle='--', label="Lagrange")
plt.plot(xp, yn, linestyle='-.', label="Newton")
plt.plot(xp, yg, linestyle=':', label="Gregory-Newton")

plt.xlabel("Dia")
plt.ylabel("Temperatura (°C)")
plt.title("Interpolação Polinomial - Comparação dos Métodos")
plt.legend()
plt.grid()
plt.show()

# =========================
# ERRO PRÁTICO (Leave-one-out)
# =========================
def erro_pratico(x, y):
    erros = []
    
    for i in range(len(x)):
        x_train = np.delete(x, i)
        y_train = np.delete(y, i)
        
        coef = newton_coef(x_train, y_train)
        y_pred = newton_eval(coef, x_train, x[i])
        
        erro = abs(y[i] - y_pred)
        erros.append(erro)
        
    return np.array(erros)

erros = erro_pratico(x, y)

print("\nErros práticos (leave-one-out):")
for i, e in enumerate(erros):
    print(f"Dia {int(x[i])}: erro = {e:.4f}")

print(f"\nErro médio: {np.mean(erros):.4f}")



# Referencias:
# [1] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.
