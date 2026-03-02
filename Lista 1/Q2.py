# ==============================================================================
# Question 2.
# ==============================================================================
# Avalie através de um gráfico o valor da função:
# f(x) = x**7 - 7*x**6 + 21*x**5 - 35*x**4 + 35*x**3 - 21*x**2 + 7*x - 1
# em 401 pontos equidistantes no intervalo [1 - 2e-8, 1 + 2e-8]. Discuta.

import matplotlib.pyplot as plt
import numpy as np

def f(x): return x**7 - 7*x**6 + 21*x**5 - 35*x**4 + 35*x**3 - 21*x**2 + 7*x - 1 # = (x-1)**7, ou seja, esperamos

Dist = ((1+(2*10**-8)) - (1-(2*10**-8)))/400 #linspace de 401, mas descobri isso só depois, evita o erro das somas sequenciais
#X = np.linspace(1-(2*10**-8), 1+(2*10**-8), 401) #linspace de 401 pontos entre 1 - 2e-8 e 1 + 2e-8

X = [1-(2*10**-8) + i*Dist for i in range(401)]
Y = [f(x) for x in X]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))


ax1.plot(X, Y, color='blue')
ax1.set_xlabel("x")
ax1.set_ylabel("f(x)")
ax1.grid(True)
ax1.axhline(0, color='black', linewidth=1.5)
ax1.axvline(1, color='red', linestyle='--', linewidth=1)

ax1.set_ylim(-1e-8, 1e-8)
ax1.set_xlim(1 - 2e-8, 1 + 2e-8)

ax2.plot(X, Y, color='blue')
ax2.set_xlabel("x")
ax2.set_ylabel("f(x)")
ax2.grid(True)
ax2.axhline(0, color='black', linewidth=1.5)
ax2.axvline(1, color='red', linestyle='--', linewidth=1)

ax2.set_ylim(-1e-14, 1e-14)
ax2.set_xlim(1 - 2e-8, 1 + 2e-8)

plt.tight_layout()
plt.show()


#No intervalo extremamente próximo de x = 1, com variação na ordem de 10^-8, o valor real da função deveria ser minúsculo, na grandeza de (10^-8)**7 = 10^-56.
# Como vimos no primeiro gráfico, na escala macro (10^-8), a curva aparenta ser uma reta perfeita no zero.
# No entanto, a distorções apresentadas quando nos aproxcimamos de 1 ocorrem, as limitaçoes de epsilon da maquina causam o cancelamento de algarismos significativos e variações de 10^-14 a 10^-16, que são os erros de arredondamento flutuando na casa do epsilon da máquina, se tornam dominantes, criando as oscilações vistas no gráfico.
