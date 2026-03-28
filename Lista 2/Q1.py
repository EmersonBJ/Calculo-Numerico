# Question 1.
# Encontre a raiz da funcao y(x) dada pelos pontos abaixo:
# X:    0      | 0.5    | 1      | 1.5    | 2      | 2.5     | 3      
# y(x): 1.8421 | 2.4694 | 2.4921 | 1.9047 | 0.8509 | -0.4112 | -1.5727
# Use interpolacao de Lagrange sobre (a) tres e (b) quatro pontos consecutivos.
# descobrir para y(x) = 0

X = [1.5, 2, 2.5]
Y = [1.9047, 0.8509, -0.4112]

# [Ref 1] Cap 3.2
def lagrange(x):
    R = 0.0  # acumulador do resultado
    for i in range(len(X)):
        # j*i = len^2 relativo a combinatoria de todos os X 2 a 2
        L_i = 1.0  # comecamos com 1 pra nao alterar o produto
        for j in range(len(X)):
            if i != j:  # quando i = j, o termo se torna 0/0, entao pulamos
                L_i *= (x - X[j]) / (X[i] - X[j])
        R += Y[i] * L_i  # soma a parcela i apos completar o produto L_i
    return R

# Para descobrirmos a raiz vamos retomar o metodo da bissecao
a = 2
b = 2.5
t = 0.0001
it = 0

while (b-a)/2 > t:
    c = (a+b)/2
    if lagrange(c) == 0:
        break
    elif lagrange(c) > 0:
        a = c
    else:
        b = c
    it += 1

print(f"A raiz aproximada e: {c:.6f}")
print(f"O numero de iteracoes foi: {it}")

# Uma alternativa para resolver a questao e usar diretamente pela biblioteca numpy
import numpy as np

# polyfit acha os coeficientes do polinomio de grau n-1 que passa exatamente pelos pontos
# para 3 pontos -> grau 2 (quadratico), equivalente ao polinomio de Lagrange

print("\n--- Equacao do Polinomio P(x) ---")
print(np.poly1d(np.polyfit(X, Y, deg=len(X)-1)))

# a propriedade .roots acha onde P(x) = 0 automaticamente
raizes = np.poly1d(np.polyfit(X, Y, deg=len(X)-1)).roots

print("\n--- Raizes Encontradas ---")
for i, raiz in enumerate(np.poly1d(np.polyfit(X, Y, deg=len(X)-1))):
    print(f"Raiz {i+1}: {raiz:.4f}")

# filtrar a raiz que faz sentido para o nosso intervalo [1.5, 2.5]
for raiz in np.poly1d(np.polyfit(X, Y, deg=len(X)-1)):
    if 1.5 <= raiz.real <= 2.5 and abs(raiz.imag) < 1e-6:
        print(f"\n=> A raiz procurada no intervalo e aproximadamente: {raiz.real:.6f}")

# A terceira alternativa seria por lagrange inverso: a logica e a mesma, so que trocamos os papeis de X e Y
# e avaliamos em y=0 para achar x diretamente, sem precisar da bissecao

# Referencias:
# [1] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.
