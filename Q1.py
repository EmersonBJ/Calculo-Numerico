#Question 1.
# ==============================================================================
# Mostre qual é o maior e o menor número flutuante que seu computador trabalha,
# realmax e realmin no MatLab.
# Mostre qual é o epsilon de sua máquina, eps no MatLab. O que quer dizer cada um destes valores?
#
# Avaliar o erro da expressão:
# f(x) = ((1 + x) - 1) / x
# Para x = {1.e-15, 1.e+15}. Calcule os erros absolutos e relativos. Discuta a diferença nos resultados.


import math
import numpy as np

#para usar o comando realmax no python, podemos usar o seguinte código:
def realmax():return np.finfo(np.float64).max #retorna o maior número representável em ponto flutuante de 64 bits (float64), esperamos algo próximo de 2^1023 * (2 - 2^(-52)) ~ 1.7976931348623157e+308
def realmin():return np.finfo(np.float64).tiny #retorna o menor número positivo representável em ponto flutuante de 64 bits (float64), esperamos algo próximo de 2^(-1022) ~ 10^(-308) ~ 2.2250738585072014e-308
def epsilon():return np.finfo(np.float64).eps #retorna a menor diferença positiva entre 1.0 e o próximo número representável em ponto flutuante de 64 bits (float64), esperamos algo próximo de 2^(-52) ~ 10^(-16) ~ 2.220446049250313e-16
#Ja que 64 bits (52 bits de precisão + 11 bits de expoente + 1 bit de sinal[IEEE 754]) tem uma precisão de aproximadamente 15-17 dígitos decimais.
# 2^52 = 10^15.95[eps], 2^11 = 2048, dividido em: 2^(-1022) ~ 10^(-308) a 2^(1023) ~ 10^(308)

def f(x):
    return (1 + x - 1)/x if x != 0 else float('inf')

V = 1

for i in [1e-15, 1e+15]:
    print(f"f({i}) = {f(i)}")
