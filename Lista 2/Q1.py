# Question 1.
# Encontre a raiz da funcao y(x) dada pelos pontos abaixo:
# X:    0      | 0.5    | 1      | 1.5    | 2      | 2.5     | 3      
# y(x): 1.8421 | 2.4694 | 2.4921 | 1.9047 | 0.8509 | -0.4112 | -1.5727
# Use interpolacao de Lagrange sobre (a) tres e (b) quatro pontos consecutivos.
# descobrir para y(x) = 0

import numpy as np
import matplotlib.pyplot as plt

X3= [1.5, 2, 2.5]
Y3= [1.9047, 0.8509, -0.4112]

X4= [1.5, 2, 2.5, 3]
Y4= [1.9047, 0.8509, -0.4112, -1.5727]

# =============================================================================
# ABORDAGEM 1: Lagrange Manual + Bissecao
# Objetivo: mostrar a logica por tras do metodo, passo a passo.
# =============================================================================

# O polinomio de Lagrange e uma soma ponderada dos valores Y pelos termos L_i(x).
# Cada L_i(x) e 1 no ponto i e 0 em todos os outros pontos — isso garante que
# o polinomio passa exatamente por todos os pontos dados.
# Formula: P(x) = sum_i [ Y_i * L_i(x) ]
#   onde:  L_i(x) = prod_{j != i} (x - X_j) / (X_i - X_j)
# [Ref 1] Cap 3.2
def calcular_raizes_lagrange(X, Y, t=1e-5):
    # 1. Função de Lagrange encapsulada para usar as listas X e Y atuais
    def lagrange(x):
        R = 0.0  # acumulador do resultado
        for i in range(len(X)):
            L_i = 1.0  # cada L_i comeca em 1 pra nao alterar o produto
            for j in range(len(X)):
                if i != j:  # quando i = j, o denominador seria 0, entao pulamos
                    L_i *= (x - X[j]) / (X[i] - X[j])
            R += Y[i] * L_i  # acumula a parcela i apos completar o produto
        return R
    
    raizes = []
    
    # 2. Varredura do domínio para encontrar os intervalos com raízes
    min_x, max_x = min(X), max(X)
    passos = 1000  # Subdivide o domínio para garantir que pegamos todas as raízes
    passo = (max_x - min_x) / passos
    
    for i in range(passos):
        a_sub = min_x + i * passo
        b_sub = a_sub + passo
        
        # Verifica se alguma raiz exata caiu direto nas bordas
        if lagrange(a_sub) == 0 and a_sub not in raizes:
            raizes.append(round(a_sub, 6))
            continue
            
        # 3. O seu algoritmo de bisseção (aplicado apenas onde há troca de sinal)
        if lagrange(a_sub) * lagrange(b_sub) < 0:
            a, b = a_sub, b_sub
            
            # Condição de parada baseada na tolerância t
            while (b - a) / 2 > t:
                c = (a + b) / 2
                
                if lagrange(c) == 0:
                    break
                # Usando troca de sinal universal
                elif lagrange(a) * lagrange(c) < 0:
                    b = c
                else:
                    a = c
            
            # Raiz encontrada e arredondada para evitar duplicações flutuantes
            raiz_encontrada = round((a + b) / 2, 6)
            if raiz_encontrada not in raizes:
                raizes.append(raiz_encontrada)

    return sorted(raizes)

# Para achar a raiz (onde P(x) = 0), usamos a bissecao.
# Sabemos que a raiz esta entre 2 e 2.5 pois Y muda de sinal nesse intervalo.
# [Ref 1] Cap 2.1



print("Abordagem 1: Lagrange Manual + Bissecao")
print(f"  (a) Raiz com 3 pontos: {calcular_raizes_lagrange(X3, Y3)}")
print(f"  (b) Raiz com 4 pontos: {calcular_raizes_lagrange(X4, Y4)}")


# =============================================================================
# ABORDAGEM 2: numpy (polyfit + poly1d)
# Objetivo: resultado compacto. Usado nos TESTES abaixo para comparacoes rapidas.
# =============================================================================

# polyfit acha os coeficientes do polinomio de grau n-1 pelos pontos dados.
# poly1d transforma esses coeficientes num objeto avaliavel e com .roots
def raiz_numpy(Xp, Yp, intervalo=(1.5, 2.5)):
    p = np.poly1d(np.polyfit(Xp, Yp, deg=len(Xp)-1))
    raizes_reais = [r.real for r in p.roots if abs(r.imag) < 1e-6 and intervalo[0] <= r.real <= intervalo[1]]
    return raizes_reais[0] if raizes_reais else None

print("\nAbordagem 2: numpy")
print(f"  (a) Raiz com 3 pontos: {raiz_numpy(X3, Y3):.6f}")
print(f"  (b) Raiz com 4 pontos: {raiz_numpy(X4, Y4):.6f}")

# =============================================================================
# ABORDAGEM 3: Interpolacao Inversa de Lagrange
# Objetivo: achar x diretamente sem bissecao, trocando os papeis de X e Y.
# x(0) = sum_i [ X_i * L_i(0) ]   onde L_i usa os Y_i como nos
# =============================================================================

def lagrange_inverso(Xp, Yp, alvo=0.0):
    raiz_x = 0.0
    for i in range(len(Xp)):
        Li = 1.0
        for j in range(len(Xp)):
            if i != j:
                Li *= (alvo - Yp[j]) / (Yp[i] - Yp[j])
        raiz_x += Xp[i] * Li
    return raiz_x


print("\nAbordagem 3: Lagrange Inverso")
print(f"  (a) Raiz com 3 pontos: {lagrange_inverso(X3, Y3):.6f}")
print(f"  (b) Raiz com 4 pontos: {lagrange_inverso(X4, Y4):.6f}")





# TESTES
# Lá no topo do arquivo, adicione:
# import matplotlib.pyplot as plt

# =============================================================================
# GRÁFICO: Curvas Aproximadas vs Pontos Exatos
# =============================================================================

Xa = [0, 0.5, 1, 1.5, 2, 2.5, 3]
Ya = [1.8421, 2.4694, 2.4921, 1.9047, 0.8509, -0.4112, -1.5727]

# Criando um eixo X contínuo - 100 pontos
x_plot = np.linspace(0, 3, 100)

p3 = np.poly1d(np.polyfit(X3, Y3, 2)) # 3 pontos = polinomio de grau 2
p4 = np.poly1d(np.polyfit(X4, Y4, 3)) # 4 pontos = polinomio de grau 3
# polyfit retorna os coeficientes do polinomio
# poly1d transforma os coeficientes num objeto avaliavel
plt.figure(figsize=(8, 5))

plt.plot(Xa, Ya, 'ko', label='Pontos Exatos (Tabela)')

plt.plot(x_plot, p3(x_plot), 'b--', label='Aproximação 3 Pontos (Parábola)')
plt.plot(x_plot, p4(x_plot), 'r-', label='Aproximação 4 Pontos (Cúbica)')

plt.axhline(0, color='gray', linestyle=':')

plt.title('Interpolação de Lagrange: Curva Exata vs Aproximações')
plt.xlabel('X')
plt.ylabel('Y(x)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.show()

# =============================================================================
#— usando Abordagem 2 (numpy) pela compacidade
# Explorando multiplos aspectos da questao
# =============================================================================

# funcao auxiliar para os testes abaixo (usa X3/Y3, os 3 pontos proximos da raiz)
def lagrange(x):
    R = 0.0
    for i in range(len(X3)):
        L_i = 1.0
        for j in range(len(X3)):
            if i != j:
                L_i *= (x - X3[j]) / (X3[i] - X3[j])
        R += Y3[i] * L_i
    return R

print("\n--- TESTE 1: Validacao da Raiz ---")
# plugamos a raiz de volta no polinomio pra confirmar que P(raiz) ≈ 0
# se o metodo funcionou, o resultado deve ser proximo de zero
raiz_ref = raiz_numpy(Xa, Ya)
p3 = np.poly1d(np.polyfit(Xa, Ya, deg=2))
p4 = np.poly1d(np.polyfit([1.5,2,2.5,3], [1.9047,0.8509,-0.4112,-1.5727], deg=3))
print(f"P3(raiz_3pts) = {p3(raiz_ref):.2e}  (esperado: ~0)")
print(f"P4(raiz_4pts) = {p4(raiz_numpy([1.5,2,2.5,3],[1.9047,0.8509,-0.4112,-1.5727])):.2e}  (esperado: ~0)")

print("\n--- TESTE 2: Convergencia da Bissecao vs Tolerancia ---")
# cada vez que apertamos a tolerancia, quantas iteracoes a mais precisamos?
# a bissecao reduz o intervalo pela metade a cada iteracao: erro = (b-a)/2^n
# entao: n ≈ log2((b-a)/tol)
for tol in [0.1, 0.01, 0.001, 0.0001, 0.00001]:
    a_, b_ = 2.0, 2.5
    n = 0
    while (b_-a_)/2 > tol:
        m = (a_+b_)/2
        if lagrange(a_) * lagrange(m) < 0:
            b_ = m
        else:
            a_ = m
        n += 1
    print(f"  tol={tol:.5f} -> {n:2d} iteracoes, raiz = {(a_+b_)/2:.6f}")

print("\n--- TESTE 3: Impacto do Numero de Pontos (grau 1 ate 6) ---")
# adicionando pontos progressivamente a partir dos mais proximos da raiz
# esperado: convergir ate certo grau, depois instabilizar (Runge)
subsets = [
    ([2.0, 2.5],                          "grau 1 (2 pts)"),
    ([1.5, 2.0, 2.5],                     "grau 2 (3 pts)"),
    ([1.5, 2.0, 2.5, 3.0],               "grau 3 (4 pts)"),
    ([1.0, 1.5, 2.0, 2.5, 3.0],          "grau 4 (5 pts)"),
    ([0.5, 1.0, 1.5, 2.0, 2.5, 3.0],    "grau 5 (6 pts)"),
    (Xa,                                   "grau 6 (7 pts)"),
]
for pts, label in subsets:
    ys = [Ya[Xa.index(x)] for x in pts]
    r = raiz_numpy(pts, ys)
    print(f"  {label:<22}: raiz = {r:.6f}" if r else f"  {label:<22}: raiz nao encontrada no intervalo")

print("\n--- TESTE 4: Sensibilidade a Erros de Medicao ---")
# simulando ruido de medicao em cada ponto e vendo o impacto na raiz
# quanto um erro de leitura em cada Y desloca a raiz estimada?
raiz_base = raiz_numpy(X3, Y3)
for idx, (xi, yi) in enumerate(zip(X3, Y3)):
    Ye = list(Y3)
    Ye[idx] = yi * 1.05
    r = raiz_numpy(X3, Ye)
    delta = r - raiz_base
    print(f"  Perturbacao de 5% em Y[x={xi}]: raiz = {r:.6f}  (delta = {delta:+.6f})")

print("\n--- TESTE 5: Bissecao com Intervalo Inicial Diferente ---")
# o que acontece se escolhermos um intervalo mais amplo ou centrado diferente?
# a bissecao deve convergir do mesmo jeito, so muda o numero de iteracoes
for ai, bi in [(1.5, 3.0), (2.0, 2.5), (2.2, 2.5), (0.0, 3.0)]:
    if lagrange(ai) * lagrange(bi) >= 0:
        print(f"  [{ai}, {bi}]: intervalo invalido (sem troca de sinal)")
        continue
    a_, b_ = ai, bi
    n = 0
    while (b_-a_)/2 > 0.0001:
        m = (a_+b_)/2
        if lagrange(a_) * lagrange(m) < 0:
            b_ = m
        else:
            a_ = m
        n += 1
    print(f"  intervalo inicial [{ai}, {bi}]: raiz = {(a_+b_)/2:.6f}  ({n} iteracoes)")

# Referencias:
# [1] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.
