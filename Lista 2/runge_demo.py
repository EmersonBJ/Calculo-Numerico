import numpy as np
import matplotlib.pyplot as plt

# Função de Runge: f(x) = 1 / (1 + 25x^2)
def runge_func(x):
    return 1 / (1 + 25 * x**2)

# 1. Definindo 5 pontos igualmente espaçados (Grau 4)
x_pontos = np.linspace(-1, 1, 5)
y_pontos = runge_func(x_pontos)

# 2. Polinômio interpolador de Lagrange (Grau 4)
# np.polyfit com deg=num_pontos-1 gera exatamente isso
p_interpol = np.poly1d(np.polyfit(x_pontos, y_pontos, 4))

# 3. Gerando pontos para as curvas contínuas
x_cont = np.linspace(-1, 1, 200)
y_real = runge_func(x_cont)
y_poly = p_interpol(x_cont)

# --- PLOT ---
plt.figure(figsize=(10, 6))

# Curva Real
plt.plot(x_cont, y_real, color='#2ca02c', label='Função Real: $1/(1+25x^2)$', linewidth=2, alpha=0.8)

# Polinômio Interpolador
plt.plot(x_cont, y_poly, color='#d62728', linestyle='--', label='Interpolador (5 pontos - Grau 4)', linewidth=2.5)

# Pontos de Amostragem
plt.scatter(x_pontos, y_pontos, color='black', s=80, zorder=5, label='Pontos Médios (Tabela)')

# Estética
plt.title('Início do Fenômeno de Runge (5 Pontos)', fontsize=14, fontweight='bold')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True, linestyle=':', alpha=0.6)
plt.axhline(0, color='black', linewidth=0.8)

# Anotação sobre o comportamento nas bordas
plt.annotate('O erro começa a crescer aqui', xy=(-0.9, 0.1), xytext=(-0.7, 0.5),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))

plt.legend(frameon=True, shadow=True)
plt.ylim(-0.2, 1.2)
plt.tight_layout()
plt.show()

# Para comparar: o que acontece com 10 pontos?
print("Observe que nas bordas (perto de x = -1 e 1) a curva vermelha começa a se distanciar da verde.")
print("Com mais pontos, essa oscilação (erro) se torna catastrófica — o Fenômeno de Runge.")
