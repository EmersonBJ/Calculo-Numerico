# Ajustamento por Mínimos Quadrados em Crescimento Populacional
# Objetivo: Usar mínimos quadrados para ajustar modelos a dados reais e interpretar o erro de aproximação.
# Descrição da Tarefa:
# 1. Utilize dados reais de crescimento populacional (procure no IBGE ou ONU).
# 2. Ajuste:
# • Um modelo polinomial (grau 2 ou 3),
# • Um modelo exponencial do tipo P(t) = a*e^(b*t).
# 3. Compare os ajustes via mínimos quadrados, apresentando os coeficientes, os resíduos e o erro quadrático
# médio.
# 4. Discuta qual modelo representa melhor os dados e em que intervalo a extrapolação pode ser confiável.
# Entrega: Código, gráficos de ajuste (dados reais vs. curva ajustada), tabela de parâmetros e relatório crítico.

import numpy as np
import matplotlib.pyplot as plt
import requests
import csv
import os

os.makedirs("Lista 2/DATA", exist_ok=True)
os.makedirs("Lista 2/graficos", exist_ok=True)

# --- IBGE via SIDRA REST API ---
print("Buscando dados reais do IBGE (SIDRA API)...")
url_ibge = "https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2001|2005|2010|2015|2019|2020|2021|2022/variaveis/9324?localidades=N1[all]"

# Fazemos a requisição. Se falhar, o r.raise_for_status() interrompe o programa na hora.
r_ibge = requests.get(url_ibge, timeout=15)
r_ibge.raise_for_status()

dados_json = r_ibge.json()
serie = dados_json[0]["resultados"][0]["series"][0]["serie"]

anos_ibge = sorted([int(k) for k in serie.keys()])
pop_ibge  = [float(serie[str(a)]) / 1e6 for a in anos_ibge]
print(f"IBGE: Sucesso! {len(anos_ibge)} registros obtidos ({anos_ibge[0]}-{anos_ibge[-1]}).")

# Salva CSV IBGE
with open("Lista 2/DATA/dados_ibge.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ano", "populacao_milhoes"])
    w.writerows(zip(anos_ibge, pop_ibge))


# --- Banco Mundial via REST API ---
print("\nBuscando dados reais do Banco Mundial...")
url_wb = "https://api.worldbank.org/v2/country/BRA/indicator/SP.POP.TOTL?format=json&per_page=100&date=1970:2022"

r_wb = requests.get(url_wb, timeout=15)
r_wb.raise_for_status()

data_list = r_wb.json()[1]
anos_censo = {1970, 1980, 1991, 2000, 2010, 2022}

# Puxa os dados apenas para os anos de censo e converte para milhões
dados_filtrados = {int(d['date']): float(d['value'])/1e6 for d in data_list if d['value'] and int(d['date']) in anos_censo}

anos_wb = sorted(dados_filtrados.keys())
pop_wb = [dados_filtrados[a] for a in anos_wb]

# Salva CSV Banco Mundial
with open("Lista 2/DATA/dados_banco_mundial.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ano_censo", "populacao_milhoes"])
    w.writerows(zip(anos_wb, pop_wb))

# ============================================================================
# 2. PREPARO PARA MINIMOS QUADRADOS
# ============================================================================

# t = decadas desde 1970 — evita numeros grandes na algebra e facilita interpretacao
# t=0 -> 1970, t=1 -> 1980, t=5.2 -> 2022, etc.
anos = np.array(anos_wb, dtype=float)
pop  = np.array(pop_wb,  dtype=float)
t    = (anos - 1970) / 10

# ============================================================================
# 3. AJUSTE POLINOMIAL - MINIMOS QUADRADOS GRAU 2
# Formula: P(t) = a*t^2 + b*t + c
# np.polyfit resolve o sistema normal A^T*A*coef = A^T*y internamente
# [Ref 1] Cap 8.1 - Quadrados Minimos Discretos
# ============================================================================

coefs_poly = np.polyfit(t, pop, 2)
poly_func  = np.poly1d(coefs_poly)
pop_poly   = poly_func(t)
res_poly   = pop - pop_poly
mse_poly   = np.mean(res_poly**2)

print("\n--- Ajuste Polinomial (grau 2) ---")
print(f"P(t) = {coefs_poly[0]:.4f}*t^2 + {coefs_poly[1]:.4f}*t + {coefs_poly[2]:.4f}")
print(f"MSE: {mse_poly:.4f}")

# ============================================================================
# 4. AJUSTE EXPONENCIAL - MINIMOS QUADRADOS
# Formula: P(t) = a * e^(b*t)
# Linearizacao: ln(P) = ln(a) + b*t -> polyfit grau 1 no log
# Depois desfazemos: a = e^(intercept), b = slope
# [Ref 1] Cap 8.1
# ============================================================================

coefs_exp = np.polyfit(t, np.log(pop), 1)
b_exp = coefs_exp[0]
a_exp = np.exp(coefs_exp[1])
pop_exp = a_exp * np.exp(b_exp * t)
res_exp = pop - pop_exp
mse_exp = np.mean(res_exp**2)

print("\n--- Ajuste Exponencial ---")
print(f"P(t) = {a_exp:.4f} * e^({b_exp:.4f}*t)")
print(f"MSE: {mse_exp:.4f}")

# ============================================================================
# 5. EXTRAPOLACAO PARA 2030
# ============================================================================

t_2030    = (2030 - 1970) / 10
prev_poly = poly_func(t_2030)
prev_exp  = a_exp * np.exp(b_exp * t_2030)

print(f"\nExtrapolacao para 2030 (t={t_2030}):")
print(f"  Polinomial  -> {prev_poly:.1f} milhoes")
print(f"  Exponencial -> {prev_exp:.1f} milhoes")

# ============================================================================
# 6. TABELA DE RESIDUOS
# ============================================================================

print("\n--- Tabela de Residuos ---")
print(f"{'Ano':<6} {'Real':>8} {'Poly':>8} {'Exp':>8} {'Res.Poly':>10} {'Res.Exp':>9}")
print("-" * 55)
for i in range(len(anos)):
    print(f"{int(anos[i]):<6} {pop[i]:>8.1f} {pop_poly[i]:>8.1f} {pop_exp[i]:>8.1f} {res_poly[i]:>+10.2f} {res_exp[i]:>+9.2f}")

melhor = "Polinomial" if mse_poly < mse_exp else "Exponencial"
print(f"\nMSE Polinomial: {mse_poly:.4f} | MSE Exponencial: {mse_exp:.4f}")
print(f"Melhor ajuste (menor MSE): {melhor}")

# ============================================================================
# 7. GRAFICO
# ============================================================================

t_plot    = np.linspace(-0.5, 7.5, 200)
anos_plot = 1970 + t_plot * 10

plt.figure(figsize=(9, 5))
plt.scatter(anos, pop, color="black", zorder=5, label="Censos IBGE/BM (dados reais)")
plt.plot(anos_plot, poly_func(t_plot),            "b-",  label=f"Polinomial grau 2  (MSE={mse_poly:.2f})")
plt.plot(anos_plot, a_exp * np.exp(b_exp*t_plot), "g--", label=f"Exponencial P=ae^(bt)  (MSE={mse_exp:.2f})")
plt.axvline(2022, color="gray", linestyle=":", alpha=0.6, label="Limite dos dados (2022)")
plt.axvline(2030, color="red",  linestyle=":", alpha=0.4, label="Extrapolacao 2030")
plt.xlabel("Ano")
plt.ylabel("Populacao (milhoes de hab.)")
plt.title("Crescimento Populacional Brasil - Minimos Quadrados")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("Lista 2/graficos/Q6_censo_brasil.png", dpi=100)
plt.show()
print("Grafico salvo em Lista 2/graficos/Q6_censo_brasil.png")

# Referencias:
# [1] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole, 2011.
# [2] IBGE. SIDRA - Sistema IBGE de Recuperacao Automatica. api.sidra.ibge.gov.br. Tabela 6579.
# [3] World Bank. Population, total (SP.POP.TOTL) - Brazil. data.worldbank.org.
