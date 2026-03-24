# Question 6.
# Ajustamento por Mínimos Quadrados em Crescimento Populacional
# Objetivo: Usar mínimos quadrados para ajustar modelos a dados reais e interpretar o erro de aproximação.
# Descrição da Tarefa:
# 1. Utilize dados reais de crescimento populacional (procure no IBGE ou ONU).
# 2. Ajuste:
#    - Um modelo polinomial (grau 2 ou 3),
#    - Um modelo exponencial do tipo P(t) = a * e^(bt).
# 3. Compare os ajustes via mínimos quadrados, apresentando os coeficientes, os resíduos e o erro quadrático médio.
# 4. Discuta qual modelo representa melhor os dados e em que intervalo a extrapolação pode ser confiável.
# Entrega: Código, gráficos de ajuste (dados reais vs. curva ajustada), tabela de parâmetros e relatório crítico.
import numpy as np
import matplotlib.pyplot as plt
import os

# Adicionando a criacao da sub-pasta para os graficos
os.makedirs("graficos", exist_ok=True)

print("--- AJUSTES MINIMOS QUADRADOS: POPULACAO DO BRASIL ---")
# amostras historicas da IBGE adaptadas p/ decadas (1 a 6) equivalentes a (1970 a 2020)
decadas = np.array([1, 2, 3, 4, 5, 6], dtype=float)
populacao = np.array([93.1, 119.0, 146.8, 169.7, 190.7, 213.3], dtype=float)

# 1. Ajuste Polinomial Mínimos Quadrados (n=2) resolvendo por least-squares da lib
# [1] Cap 8.1 - Quadrados Minimos Discretos
coefs_poly = np.polyfit(decadas, populacao, 2)
# equacao tipo ax^2 + bx + c
poly_func = np.poly1d(coefs_poly)
pop_poly = poly_func(decadas)

# 2. Ajuste Exponencial Minimos Quadrados
# linearizar a funcao exponencial (ln_y = ln_a + bx)
ln_populacao = np.log(populacao)
coefs_exp = np.polyfit(decadas, ln_populacao, 1)

# desfaz a linearizacao pra encontrar os thetas reias da modelo
b_exp = coefs_exp[0]
a_exp = np.exp(coefs_exp[1])
# reconstroi a curva real P(t) = a * e^(b*t)
pop_exp = a_exp * np.exp(b_exp * decadas)

# analise quantitativa (Mean Squared Error) para conferir acuracia do ajuste
mse_poly = np.mean((populacao - pop_poly)**2)
mse_exp = np.mean((populacao - pop_exp)**2)

print("\nComparativo de Ajustes e Resíduos:")
print(f"MSE Polinômio de Grau 2: {mse_poly:.4f}")
print(f"MSE Exponencial Linear:  {mse_exp:.4f}")

ano_previsao = 7 # estimativa decada (2030)
prev_poly = poly_func(ano_previsao)
prev_exp = a_exp * np.exp(b_exp * ano_previsao)

print(f"\nExtrapolação Prevista para a década {ano_previsao} (2030):")
print(f"Predição Polinomial   -> {prev_poly:.1f} milhões")
print(f"Predição Exponencial  -> {prev_exp:.1f} milhões")

# Plotando os resultados com matplotlib pra entregar visualmente as regressoes
x_plot = np.linspace(0.5, 7.5, 100)
plt.figure(figsize=(8, 5))
plt.scatter(decadas, populacao, color='black', label='Censos (Historico IBGE)', zorder=5)
plt.plot(x_plot, poly_func(x_plot), 'b-', label='Modelagem MinSQ Polinomial')
plt.plot(x_plot, a_exp * np.exp(b_exp * x_plot), 'g--', label='Modelagem MinSQ Exponencial')
plt.title("Evolução Demográfica vs Mínimos Quadrados")
plt.xlabel("Décadas decorridas de 1970")
plt.ylabel("Índice Pop. (Milhões hab.)")
plt.legend()
plt.grid(True)
plt.savefig("graficos/Q6_censo_brasil.png", dpi=100)

print("\n> Grafico plotado e documentado na pasta 'graficos' como 'Q6_censo_brasil.png'.")
print("> [Relatório Crítico]: O MSE polinomial é muito baixo provindo superaderência, porém extrapolações além de t=7 podem decair bruscamente. O modelo exponencial extrapola melhor a longo prazo sem infletir as curvas.")

# Referencias:
# [1] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.