import math
import sympy as sp

x = sp.symbols('x')
# Para resolver equações transcendentais no sympy, usamos sp.log e nsolve para valor numérico
equacao = sp.log(x + 1) + x - 2
raiz_num = sp.nsolve(equacao, x, 1.0)
print(f"Raiz encontrada via SymPy: {raiz_num}")

class Func1:
    Raizes = [1, 2, -3]
    
    @staticmethod
    def f(x): return x**3 - 7*x + 6
    @staticmethod
    def df(x): return 3*x**2 - 7
    @staticmethod
    def phi(x): return (x**3 + 6)/7
    @staticmethod
    def dphi(x): return (3*x**2)/7

class Func2:
    Raizes = [float(raiz_num)] 
    
    @staticmethod
    def g(x): return math.log(x + 1) + x - 2
    @staticmethod
    def dg(x): return 1/(x + 1) + 1
    @staticmethod
    def phi_g(x): return 2 - math.log(x + 1)
    @staticmethod
    def dphi_g(x): return -1/(x + 1)
