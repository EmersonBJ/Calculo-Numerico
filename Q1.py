import math
import numpy as np

#para usar o comando realmax no python, podemos usar o seguinte código:
def realmax():return np.finfo(np.float64).max
def realmin():return np.finfo(np.float64).tiny
def epsilon():return np.finfo(np.float64).eps

print(f"Realmax: {realmax()}; Realmin: {realmin()}; Epsilon: {epsilon()}")

def f(x):
    return (1 + x - 1)/x if x != 0 else float('inf')

V = 1

for i in [1e-15, 1e+15]:
    print(f"f({i}) = {f(i)}")