
# O Impacto dos Erros de Arredondamento na Busca de Raízes
# Objetivo: Explorar como erros de arredondamento e truncamento influenciam a convergência dos métodos
# de busca de zeros.
# Descrição da Tarefa:
# 1. Escolha uma função simples, como f(x) = e^x − 2 ou f(x) = cos(x) − x.
import math
def f(x):
    return math.exp(x) - 2 
def g(x):
    return math.cos(x) - x

# 2. Programe os métodos da bisseção e da Falsa Posição.
# O método da bisseção (eq. 2.1 do livro [1]) e a Regula Falsi (eq. 2.3 do livro [2]) são métodos de busca de raízes que utilizam intervalos para encontrar soluções aproximadas. O método da bisseção divide o intervalo em duas partes iguais e seleciona o subintervalo onde a função muda de sinal, enquanto o método da falsa posição utiliza uma linha reta (secante) para aproximar a função e encontrar a raiz.


# Método de bisseção
# Selecionamos extremos em uma função que garantam a existência de uma raiz entre eles, tal que f(a) e f(b) tenham sinais opostos. Pelo Teorema de Bolzano (Seção 2.1 [1] e Seção de revisão em cálculo 1.1 [2]), podemos garantir que, se o produto das funções for menor que zero, haverá ao menos uma raiz entre esses dois pontos.
# [1] x^(k) = [a^(k) + b^(k)] / 2
# Variáveis para g(x):
k = 0
# algoritimo para escolher a e b de forma a garnatir que f(a)*f(b)< 0
achou = False # Uma bandeira para parar tudo

#for i in range(-100, 0):          # Testa negativos para 'a'
    #for j in range(0, 100):       # Testa positivos para 'b'
        # Garante que encontraremos a raiz desde que ela esteja entre (-100, 100)
        
        #if f(i) * f(j) < 0:     #salva o intervalo
            #a = i
           # b = j
           # achou = True
           # print(f"Intervalo encontrado: [{a}, {b}]")
            #break 
        #else:
            #continue
a, b = -2, 2
            
# * Testar se conseguimos salvar em um vetor todos os pares (a, b) para encontrar múltiplas raízes.
# * Criterios de parada:
# 1. Tolerância no erro absoluto: |f(b) - f(a)| < t
# 2. Tolerância no valor da função: |f(c)| < t
# 3. Tolerância no erro relativo: |b - a| / |a| < t
# 4. Número máximo de iterações (para evitar loops infinitos)
# 5. Valor exato encontrado: f(c) == 0
import numpy as np
ab, bb = a, b # Salva os valores originais de a e b para usar no método da falsa posição.        
t = 0.00000000000001 # Tolerância para testar quando começam as inconsistências.
Ib = 0 # Contador de iterações para o método da bisseção.
# Testaremos os valores de 0 até 2 para a raiz, (atualizei o mecanismos para que ele encontre sozinho).

errors_B_float64 = []
errors_B_float32 = []
errors_B_trunc = []

while abs(f(bb) - f(ab)) > t:  # Erro < tolerancia

    Ib += 1 # Contador de iterações (Para o item 4)
    c = (ab + bb)/2

    errors_B_float64.append(abs(f(c)))
    errors_B_float32.append(abs(np.float32(f(c))))
    errors_B_trunc.append(abs(math.trunc(f(c)*10e4)/10e4))

    if f(c) == 0: # Confere se achamos a raiz exata dentro da precisão de 64 bits (aprox. 16 dígitos).
        break
    elif f(ab) * f(c) < 0:
        bb = c
    else:
        ab = c
print(f"f(c) = {f(c):.50f}, c = {c:.50f}") # Uso de 50 casas decimais para observar inconsistências ao variar "t".
# *Podemos notar inconsistências no resultado ao nos aproximarmos do limite do sistema x64; o valor pode chegar a ser interpretado como zero absoluto.
# *Convergencia Linear





# Método Falsa Posição
# Variação do método da bisseção que costuma convergir mais rápido.
# O método avalia quão próximo o resultado está de zero. Os pontos 'a' e 'b' definem uma reta secante cuja intersecção com o eixo x fornece a nova aproximação.
# [2] p = b - f(b) * (b-a)/[f(b)-f(a)]
# Podemos usar o mesmo princípio de Bolzano, porém mudando a forma de calcular o ponto intermediário entre 'a' e 'b'.
def h(x):
    return f(x)
p = a
Ip = 0 # Contador de iterações para o método da falsa posição.
ap, bp = a, b # Salva os valores originais de a e b para usar no método da falsa posição.

errors_FP_float64 = []
errors_FP_float32 = []
errors_FP_trunc = []


while abs(h(bp) - h(ap)) > t: 
    Ip += 1 # Contador de iterações (Para o item 4)
    p = bp - ((h(bp) * (bp - ap))/(h(bp)- h(ap))) # Diferença: em vez do ponto médio, usa-se a interpolação linear.
   
    errors_FP_float64.append(abs(h(p)))
    errors_FP_float32.append(abs(np.float32(h(p))))
    errors_FP_trunc.append(abs(math.trunc(h(p)*10000)/10000))

    if h(p) == 0:
        break
    elif h(ap)*h(p) < 0:
        bp = p
    else:
        ap = p
print(f"f(p) = {h(p):.50f}, p = {p:.50f} com algoritmo de Falsa Posição")


# 3. Implemente as operações usando:
# • Ponto flutuante com precisão normal (float64),
# • Ponto flutuante com precisão reduzida (float32),
# • Simulação de truncamento (4 casas decimais). (eq. 1.1 e 1.2 do livro[2])
# *ξ(x) é um número entre x e x0(seção 1.1 do livro [2])*
#import numpy as np
print(f"Bisseção - f(c) Float 64: {float(f(c)):.20f} | Float 32: {np.float32(f(c)):.20f} | Truncamento - F(C) 4 casas decimais:{math.trunc(f(c)*10e4)/10e4:.20f}") # Float64, float32 e truncamento 4f
print(f"Falsa Posição - h(p) Float 64: {float(h(p)):.20f} | Float 32: {np.float32(h(p)):.20f} | Truncamento - H(p) 4 casas decimais:{math.trunc(h(p)*10e4)/10e4:.20f}")

# A precisão de 32 bits reduz significativamente o número de casas decimais confiáveis.
# O truncamento não é o mesmo que arredondamento (eq 1.1 e 1.2). Para simular o truncamento de 4 casas decimais, evitamos a função 'round' e utilizamos 'math.trunc' para remover os dígitos excedentes sem ajustar o último dígito mantido.

# 4. Compare como a precisão influencia o número de iterações e o erro final.
# Entrega: Código em Python ou outra linguagem, tabelas e gráficos mostrando convergência, discussão sobre estabilidade numérica.
#Ambos os livros definem uma iteração como um passo num processo repetitivo onde a aproximação atual xk​ é usada para calcular uma nova aproximação x k+1​ , gerando uma sequência {xk​} que esperamos convergir para a solução exata α.
import matplotlib.pyplot as plt
# Para comparar a convergência, podemos criar gráficos do erro em função do número de iterações para cada método e cada tipo de precisão(float64, float32 e truncamento). O erro pode ser calculado como |f(c)| ou |h(p)|, dependendo do método.
# Exemplo de gráfico para o método da bisseção:
# Gerar dados para o gráfico
#errors_B_float64 = [] -> errors_B_float64.append(abs(f(c)))
#errors_B_float32 = [] -> errors_B_float32.append(abs(np.float32(f(c))))
#errors_B_trunc = []   -> errors_B_trunc.append(abs(math.trunc(f(c)*10e4)/10e4))
#Primeiramente criam uma lista vazia para cada tipo de erro e, dentro do loop de iteração, adicionam o erro correspondente a cada lista. Depois, podemos plotar esses erros em um gráfico de linha para visualizar a convergência.

#Gerar graficos
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(range(1, len(errors_B_float64)+1), errors_B_float64, label='Bisseção - Float64')
plt.plot(range(1, len(errors_FP_float64)+1), errors_FP_float64, label='Falsa Posição - Float64')
plt.xlabel('Iterações')
plt.ylabel('Erro')
plt.title('Convergência - Float64')
plt.legend()
plt.grid(True)
#Regem as configuraçoes basicas do grafico: tamanho, eixos, título, legenda e grade. O mesmo processo é repetido para o gráfico de precisão reduzida (float32) e truncamento.

plt.subplot(1, 2, 2)
plt.plot(range(1, len(errors_B_float32)+1), errors_B_float32, label='Bisseção - Float32')
plt.plot(range(1, len(errors_FP_float32)+1), errors_FP_float32, label='Falsa Posição - Float32')
plt.xlabel('Iterações')
plt.ylabel('Erro')
plt.title('Convergência - Float32')
plt.legend()
plt.grid(True)

# Exibir os gráficos
plt.tight_layout()
plt.show()


# Referência:
# [1] QUARTERONI, Alfio; SALERI, Fausto. Scientific computing with MATLAB and Octave. 2. ed. Berlin: Springer, 2006. (Texts in computational science and engineering, 2).
# [2] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.