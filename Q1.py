import math
import numpy as np

#para usar o comando realmax no python, podemos usar o seguinte código:
def realmax():return np.finfo(np.float64).max
def realmin():return np.finfo(np.float64).min
def epsilon(): return np.finfo(np.float64).eps

print(f"Realmax: {realmax()}; Realmin: {realmin()}; Epsilon: {epsilon()}")