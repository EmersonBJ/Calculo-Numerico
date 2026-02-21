# ==============================================================================
# Question 2.
# ==============================================================================
# Avalie através de um gráfico o valor da função:
# f(x) = x**7 - 7*x**6 + 21*x**5 - 35*x**4 + 35*x**3 - 21*x**2 + 7*x - 1
# em 401 pontos equidistantes no intervalo [1 - 2e-8, 1 + 2e-8]. Discuta.

import matplotlib.pyplot as plt

def f(x): return x**7 - 7*x**6 + 21*x**5 - 35*x**4 + 35*x**3 - 21*x**2 + 7*x - 1 # = (x-1)**7, ou seja, esperamos

Dist = ((1+(2*10**-8)) - (1-(2*10**-8)))/400 #linspace de 401, mas descobri isso só depois

X = [1-(2*10**-8) + i*Dist for i in range(401)]
Y = [f(x) for x in X]

plt.plot(X, Y)
plt.title("Gráfico de f(x) no intervalo [1 - 2e-8, 1 + 2e-8]")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)


plt.axhline(0, color='black', linewidth=1.5) 
plt.axvline(1, color='red', linestyle='--', linewidth=1) 

plt.show()