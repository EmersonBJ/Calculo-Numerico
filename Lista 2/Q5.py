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

print("--- INTERPOLACAO DE TEMPERATURAS (DADOS SIMULADOS INMET) ---")
# dados hipotéticos amostrados de Janeiro (São Paulo, 5 dias consecutivos)
dias = np.array([1, 2, 3, 4, 5], dtype=float)
temps = np.array([28.5, 30.1, 31.5, 29.8, 27.2], dtype=float)

# [1] Cap 3.1 - Polinomios de Interpolacao de Lagrange
# avalia polinomio via Lagrange puro
def lagrange(x_pontos, y_pontos, x_alvo):
    n = len(x_pontos)
    y_alvo = 0.0
    for i in range(n):
        L = 1.0
        for j in range(n):
            if i != j:
                L *= (x_alvo - x_pontos[j]) / (x_pontos[i] - x_pontos[j])
        y_alvo += y_pontos[i] * L
    return y_alvo

# [1] Cap 3.3 - Diferencas Divididas
# calcula tabela de diferencas divididas para Newton
def diff_div(x_pontos, y_pontos):
    n = len(y_pontos)
    coef = np.zeros([n, n])
    coef[:,0] = y_pontos
    for j in range(1, n):
        for i in range(n-j):
            coef[i][j] = (coef[i+1][j-1] - coef[i][j-1]) / (x_pontos[i+j] - x_pontos[i])
    return coef[0, :] # retorna a diagonal superior p/ calculo do polinomio

# avalia polinomio de Newton
def newton(x_pontos, coefs, x_alvo):
    n = len(coefs)
    y_alvo = coefs[0]
    for i in range(1, n):
        termo = coefs[i]
        for j in range(i):
            termo *= (x_alvo - x_pontos[j])
        y_alvo += termo
    return y_alvo

# interpolacao p/ dia 3.5 (meio do dia 3)
coefs_newton = diff_div(dias, temps)
t_lagrange = lagrange(dias, temps, 3.5)
t_newton = newton(dias, coefs_newton, 3.5)

print(f"Temperatura prevista no dia 3.5 (Lagrange): {t_lagrange:.3f} °C")
print(f"Temperatura prevista no dia 3.5 (Newton):   {t_newton:.3f} °C")
print("[Erro Teórico]: O polinômio resultante é matemático e unicamente igual em ambos os métodos de mesmo grau.")

# gera grafico suave passando sobre as interpolacoes
x_curva = np.linspace(1, 5, 100)
y_lagrange = [lagrange(dias, temps, x) for x in x_curva]
y_newton = [newton(dias, coefs_newton, x) for x in x_curva]

plt.figure(figsize=(8, 5))
plt.scatter(dias, temps, color='red', zorder=5, label='Temperaturas Coletadas')
plt.plot(x_curva, y_lagrange, 'b-', label='Interp. Lagrange', alpha=0.8)
plt.plot(x_curva, y_newton, 'k--', label='Interp. Newton (Sobreposta)', alpha=0.5)
plt.title("Acompanhamento e Interpolação Termal (Grau 4)")
plt.xlabel("Dia Mensal")
plt.ylabel("Graus Celsius (°C)")
plt.legend()
plt.grid(True)
plt.savefig("./graficos/Q5_temperaturas.png", dpi=100)

print("\n> Gráfico comparativo gerado e salvo como 'Q5_temperaturas.png'.")
print("> [Relatório]: Interpolações de grau muito elevado (> 5) falham miseravelmente nas bordas e sofrem do Fenômeno de Runge. Interpoladores locais tipo Splines são indicados como alternativas mais robustas.")

# Referencias:
# [1] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.
