

class Func1:
    def f(self, x): return x**3 - 7*x + 6
    #f'(x) = 3*x**2 - 7
    def df(self, x): return 3*x**2 - 7
    #Para comparaçao de erros:
    Raizes = [1, 2, -3] 
    def phi(self, x): return (x**3 +6)/7
    def dphi(self, x): return (3*x**2)/7

class Func2:
    def g(self, x): return math.log(x + 1) + x - 2
    def dg(self, x): return 1/(x + 1) + 1
    Raizes = [1.20794] 

    def phi_g(self, x): return 2 - math.log(x + 1)
    def dphi_g(self, x): return -1/(x + 1)

g = 9.81
L = 1
T = 2.0 #Período observado arbitrário.

import math
Raizes = math.asin((T / (2 * math.pi)) * math.sqrt(g / L))
print(Raizes)