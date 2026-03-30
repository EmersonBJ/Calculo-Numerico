# Ajustamento por Mínimos Quadrados em Crescimento Populacional
# Objetivo: Usar mínimos quadrados para ajustar modelos a dados reais e interpretar o erro de aproximação.
# Descrição da Tarefa:
# 1. Utilize dados reais de crescimento populacional (procure no IBGE ou ONU).
# 2. Ajuste:
# • Um modelo polinomial (grau 2 ou 3),
# • Um modelo exponencial do tipo P(t) = a*e^(b*t).
# 3. Compare os ajustes via mínimos quadrados, apresentando os coeficientes, os resíduos e o erro quadrático médio.
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
# Fazemos a requisição. Se falhar, o r.raise_for_status() interrompe o programa na hora.
r_ibge = requests.get("https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2001|2005|2010|2015|2019|2020|2021|2022/variaveis/9324?localidades=N1[all]")

r_ibge.raise_for_status()

serie = r_ibge.json()[0]["resultados"][0]["series"][0]["serie"]

anos_ibge = sorted([int(k) for k in serie.keys()])
pop_ibge  = [float(serie[str(a)]) / 1e6 for a in anos_ibge]

with open("Lista 2/DATA/dados_ibge.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ano", "populacao_milhoes"])
    w.writerows(zip(anos_ibge, pop_ibge))


# --- Banco Mundial via REST API ---


r_wb = requests.get("https://api.worldbank.org/v2/country/BRA/indicator/SP.POP.TOTL?format=json&per_page=100&date=1970:2022")
r_wb.raise_for_status()

data_list = r_wb.json()[1]
anos_censo = {1970, 1980, 1991, 2000, 2010, 2022}

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
# Tentamos mesclar os dados do IBGE e do Banco Mundial, mas a diferencas metodologicas tornam a curva muito irregular, entao optamos por usar apenas os dados do Banco Mundial.

anos = np.array(anos_wb, dtype=float)
pop  = np.array(pop_wb,  dtype=float)
t    = (anos - 1970) / 10

#polyfit constrói a fórmula: Ele olha os dados e diz "A melhor equação é 2x^2 +3x+5". Ele te devolve os coeficientes [2, 3, 5].
#polyval usa a fórmula: Ele pega esses coeficientes [2, 3, 5] e um valor de x (por exemplo, x=10) e faz a conta por você: 2(10)^2 +3(10)+5=235.

# • Um modelo polinomial (grau 2 ou 3)
#np.polyfit(t, pop, 2) grau 2
coefs2 = np.polyfit(t, pop, 2)
MG2 = np.polyval(coefs2, t)  # predicao nos 6 pontos do censo (para calcular residuos)
Res2 = pop - MG2
EQM2 = np.mean(Res2**2)

#np.polyfit(t, pop, 3) grau 3
coefs3 = np.polyfit(t, pop, 3)
MG3 = np.polyval(coefs3, t)  # predicao nos 6 pontos do censo
Res3 = pop - MG3
EQM3 = np.mean(Res3**2)

# • Um modelo exponencial do tipo P(t) = a*e^(b*t).
# P(t) = a*e^(b*t) -> ln(P(t)) = ln(a) + b*t
#np.polyfit(t, np.log(pop), 1) exponencial
m = np.polyfit(t, np.log(pop), 1)
b = m[0]
a = np.exp(m[1])

MG_exp = a * np.exp(b * t)
Res_exp = pop - MG_exp
EQM_exp = np.mean(Res_exp**2)

# 3. Compare os resultados e discuta a unicidade do polinômio interpolador.

#GRÁFICO (DADOS REAIS VS. CURVAS AJUSTADAS)
plt.figure(figsize=(10, 6))

anos_plot = np.linspace(anos.min(), anos.max(), 300)
t_plot = (anos_plot - 1970) / 10  # t_plot tem 300 pontos — mesma dimensao de anos_plot

plt.plot(anos, pop, 'ko',                                                       label='Dados Reais',        markersize=7)
plt.plot(anos_plot, np.polyval(coefs2, t_plot), 'b--',   linewidth=2,            label='Polinômio Grau 2')   # azul tracejado
plt.plot(anos_plot, np.polyval(coefs3, t_plot), 'g-.',   linewidth=2,            label='Polinômio Grau 3')   # verde traco-ponto
plt.plot(anos_plot, a * np.exp(b * t_plot),     'r:',    linewidth=2.5,          label='Exponencial')         # vermelho pontilhado

plt.xlabel('Ano')
plt.ylabel('População (milhões)')
plt.title('Ajustamento por Mínimos Quadrados em Crescimento Populacional')
plt.legend()
plt.grid(True)
plt.savefig('Lista 2/graficos/crescimento_populacional.png')
plt.show()


# TABELA DE PARÂMETROS E ERROS
print("\n" + "="*80)
print("TABELA DE PARÂMETROS E ERROS (EQM)")
print("="*80)
print(f"{'Modelo':<20} | {'Coeficientes':<40} | {'EQM':<10}")
print("-" * 80)
# Usei np.round para o print não ficar gigante na tela
print(f"{'Polinômio Grau 2':<20} | {np.round(coefs2, 4)} | {EQM2:.6f}")
print(f"{'Polinômio Grau 3':<20} | {np.round(coefs3, 4)} | {EQM3:.6f}")
print(f"{'Exponencial':<20} | a={a:.4f}, b={b:.4f} | {EQM_exp:.6f}")
print("=" * 80)

# APRESENTAÇÃO DOS RESÍDUOS (Requisito 3)
print("\nRESÍDUOS (Diferença entre Dado Real e Curva Ajustada por década):")
print(f"- Polinômio Grau 2: {np.round(Res2, 4)}")
print(f"- Polinômio Grau 3: {np.round(Res3, 4)}")
print(f"- Exponencial:      {np.round(Res_exp, 4)}")

#RELATÓRIO CRÍTICO
print("\n" + "="*60)
print("RELATÓRIO CRÍTICO")
print("="*60)
print("\n1. Comparação dos Ajustes:")
print(f"   - Polinômio Grau 2: EQM = {EQM2:.6f}")
print(f"   - Polinômio Grau 3: EQM = {EQM3:.6f}")
print(f"   - Exponencial: EQM = {EQM_exp:.6f}")
