# O Impacto dos Erros de Arredondamento na Busca de Raízes
# Objetivo: Explorar como erros de arredondamento e truncamento influenciam a convergência dos métodos
# de busca de zeros.
# Descrição da Tarefa:
# 1. Escolha uma função simples, como f(x) = e^x − 2 ou f(x) = cos(x) − x.
# 2. Programe os métodos da bisseção e da Falsa Posição.
# O método da bisseção (eq. 2.1 do livro [1]) e a Falsa Posição (eq. 2.3 do livro [2]) são métodos de busca de raízes que utilizam intervalos para encontrar soluções aproximadas. O método da bisseção divide o intervalo em duas partes iguais e seleciona o subintervalo onde a função muda de sinal, enquanto o método da falsa posição utiliza uma linha reta (secante) para aproximar a função e encontrar a raiz.
# * Testar se conseguimos salvar em um vetor todos os pares (a, b) para encontrar múltiplas raízes. [fiz no arquivo de rascunho, mas não é necessário para a função escolhida, que tem apenas uma raiz real, então optei por deixar o código mais simples e direto para o caso específico]
# * Criterios de parada:

# 1. Tolerância no erro absoluto: |f(b) - f(a)| < t
# 2. Tolerância no valor da função: |f(c)| < t
# 3. Número máximo de iterações (para evitar loops infinitos) [*]
# 4. Valor exato encontrado: f(c) == 0 -Adicionado-

# 3. Implemente as operações usando:
# • Ponto flutuante com precisão normal (float64),
# • Ponto flutuante com precisão reduzida (float32),
# • Simulação de truncamento (4 casas decimais). (eq. 1.1 e 1.2 do livro[2])

# Como modifiquei as definições das funções para incluir o modo de operação, podemos facilmente comparar os resultados dos métodos de bisseção e falsa posição usando as três formas de precisão. A função 'f' agora aceita um argumento 'mode' que determina como os cálculos são realizados, permitindo uma análise direta do impacto dos erros de arredondamento e truncamento em cada etapa do processo.

# A precisão de 32 bits reduz significativamente o número de casas decimais confiáveis.
# O truncamento não é o mesmo que arredondamento (eq 1.1 e 1.2). Para simular o truncamento de 4 casas decimais, evitamos a função 'round' e utilizamos 'math.trunc' para remover os dígitos excedentes sem ajustar o último dígito mantido.

# 4. Compare como a precisão influencia o número de iterações e o erro final.
# Entrega: Código em Python ou outra linguagem, tabelas e gráficos mostrando convergência, discussão sobre estabilidade numérica.


# Reescrevi a função definindo desde o começo os três tipos de precisão para facilitar a comparação posterior. A função f(x) é definida para retornar os valores em float64, float32 e truncado, dependendo do modo selecionado. 
# Dessa forma evitamos que o erro seja visto apenas na conta final, mas sim em cada etapa do processo, o que é mais realista para entender o impacto dos erros de arredondamento e truncamento.
import numpy as np
import math

def f(x, mode='float64'):
    if mode == 'math.trunc': 
        return math.trunc(((math.exp(x)) - 2)*10e3)/10e3 # Truncamento com 4 casas decimais
    
    elif mode == 'float32':
        return np.float32(np.exp(x) - 2)
    
    return math.exp(x) - 2 # Valor em float64 por padrão, que é a precisão normal do Python.

# f(x) =  e^x - 2 ->  x * log(e) = log(2) -> x = log(2) -> raiz = log(2)
raiz = math.log(2) # raiz exata para comparação de erros
(a,b,t) = -2, 2, 0.0000000000000001



# Método de bisseção
# Selecionamos extremos em uma função que garantam a existência de uma raiz entre eles, tal que f(a) e f(b) tenham sinais opostos. Pelo Teorema de Bolzano (Seção 2.1 [1] e Seção de revisão em cálculo 1.1 [2]), podemos garantir que, se o produto das funções for menor que zero, haverá ao menos uma raiz entre esses dois pontos.
# [1] x^(k) = [a^(k) + b^(k)] / 2

def bissecao(a, b, t, mode='float64'): # aqui eu apenas juntei todas as 3 contas em um definidor, para poder facilmente mudar os parâmetros.
    # Aqui a, b e t são os parâmetros de entrada, e mode determina a precisão utilizada (float64, float32 ou truncamento).
    it = 0 # contador de iterações
    e = [] # lista para armazenar os erros em cada iteração, para análise posterior.


    while abs(b - a) > t and it < 100: # (critério de parada 1 e 2)
        #Parametros iniciais:
        x = (a + b) / 2 # Equação da bisseção para calcular o ponto médio entre a e b.
        it +=1

        #Garantir precisao do resultado:
        if mode == 'math.trunc': # Se escolhermos o modo de truncamento, aplicamos a função de truncamento ao x (resultado da bisseção) para simular a perda de precisão.
            x = math.trunc(x * 10e3) / 10e3
        elif mode == 'float32': # Se escolhermos o modo de float32, convertemos x para float32 para simular a precisão reduzida.
            x = np.float32(x)
        elif mode == 'float64': # Redundância para garantir que o modo float64 seja aplicado, embora seja o padrão.
            pass

        e.append(float(abs(x - raiz))) # Armazena o erro absoluto em relação à raiz exata para análise de convergência.

        if f(x, mode) == 0: # Observa se encontramos a raiz exata, o que é improvável, mas possível.
            return float(x), it, e
        
        elif f(a, mode) * f(x, mode) < 0: # Regra de Bolzano, acompanhada do modo de precisão selecionado.
            b = x # Se a função muda de sinal entre a e x, então a raiz está entre a e x, b desce para x.

        else:
            a = x # Caso contrário, a raiz está entre x e b, então a sobe para x.

    return float(x), it, e # Retorna a aproximação da raiz e o número de iterações realizadas.

B = [bissecao(a,b,t, mode='float64'), bissecao(a,b,t, mode='float32'), bissecao(a,b,t, mode='math.trunc')]
# a = -2, b = 2, t = 10e3, modo float64,  a = -2, b = 2, t = 10e3, modo float32, a = -2, b = 2, t = 10e3, modo truncamento (4 casas decimais)
# Salvo no vetor B. Para cada item do vetor teremos 3 coordenadas: a aproximação da raiz (x), o número de iterações (it) e o vetor de erros para análise de convergência (e).

print("Bisseção com float64 e Iterações:", B[0]), print("Bisseção com float32 e Iterações:", B[1]), print("Bisseção com truncamento e Iterações:", B[2])
# Pra registro: além dos problemas que tive na elaboração do rascunho, temos alguns problemas na criação dos vetores.
# No modo de truncamento, parece ser muito pequeno e ele não cria uma lista, o que me dá problema na hora de ler tudo de uma só vez na elaboração do gráfico. Posso optar por fazê-los separadamente ou tentar forçar a adição de um 0 quando o modo for truncamento *corrigiu sozinho*.
# Além disso, a opção float32 é registrada no vetor como nome e não função tal qual "float32(xxx)", vou contornar forçando a conversão para float antes de salvar, o que não deve alterar o resultado final uma vez que a conta já foi feita em x32.








# Método Falsa Posição
# Variação do método da bisseção que costuma convergir mais rápido.
# O método avalia quão próximo o resultado está de zero. Os pontos 'a' e 'b' definem uma reta secante cuja intersecção com o eixo x fornece a nova aproximação.
# [2] p = b - f(b) * (b-a)/[f(b)-f(a)]
# Podemos usar o mesmo princípio de Bolzano, porém mudando a forma de calcular o ponto intermediário entre 'a' e 'b'.


def falsa_posicao(a, b, t, mode='float64'): # Assim como na função de bisseção, a função de falsa posição recebe os mesmos parâmetros de entrada, permitindo uma comparação direta entre os dois métodos sob as mesmas condições de precisão e tolerância.
    it = 0 # Como o resultado já foi apresentado pelo return anterior, eu reciclei a variável de iteração para usar aqui, evitando criar uma nova variável desnecessária.
    x = a
    e = [] # Lista para armazenar os erros em cada iteração, para análise posterior.

    while it < 100: # Aproximação é menor que a tolerância ou Limitada a 100 iterações (critério de parada 1 e 2)
        # Problema de lógica: usando o 'while', a condição de continuação é a negação da condição de parada. Se queremos parar quando a distância for menor que a tolerância OU quando o número de iterações exceder 100, o loop deve continuar enquanto a distância for maior que a tolerância E o número de iterações for menor que 100.
        # O argumento de parada de A é ¬(A)
        it += 1
        
        
        # Fórmula da falsa Posição
        p = (a * f(b, mode) - b * f(a, mode)) / (f(b, mode) - f(a, mode))
        
        if mode == 'math.trunc': p = math.trunc(p*10e3)/10e3
        if mode == 'float32': p = np.float32(p)
        if mode == 'float64': pass

        e.append(float(abs(p - raiz))) # Armazena o erro absoluto em relação à raiz exata para análise de convergência.
        if abs(f(p, mode)) < t: return float(p), it, e

        if f(x, mode) == 0: # Observa se encontramos a raiz exata, o que é improvável, mas possível.
            return float(x), it, e

        if f(a, mode) * f(p, mode) < 0:
            b = p

        else:
            a = p
            
        x = p
    return float(x), it, e

F = [falsa_posicao(a,b,t, mode='float64'), falsa_posicao(a,b,t, mode='float32'), falsa_posicao(a,b,t, mode='math.trunc')]

# a = -2, b = 2, t = 10e3, modo float64,  a = -2, b = 2, t = 10e3, modo float32, a = -2, b = 2, t = 10e3, modo truncamento (4 casas decimais)
# Salvos no vetor F, que também terá 3 coordenadas para cada item: a aproximação da raiz (x), o número de iterações (it) e o vetor de erros para análise de convergência (erros).

print("Falsa Posição com float64 e Iterações:", F[0]), print("Falsa Posição com float32 e Iterações:", F[1]), print("Falsa Posição com truncamento e Iterações:", F[2]) 




# Tabela de Dados, para análise de consistência
import pandas as pd

data_struct = {
    'Método': ['Bisseção']*3 + ['Falsa Posição']*3,
    'Modo': ['Float64', 'Float32', 'Trunc']*2,
    'Raiz Final': [B[0][0], B[1][0], B[2][0], F[0][0], F[1][0], F[2][0]],
    'Iterações': [B[0][1], B[1][1], B[2][1], F[0][1], F[1][1], F[2][1]],
    'Erro Final': [B[0][2][-1], B[1][2][-1], B[2][2][-1], 
                   F[0][2][-1] if F[0][2] else 0, 
                   F[1][2][-1] if F[1][2] else 0, 
                   F[2][2][-1] if F[2][2] else 0]
}

pd.DataFrame(data_struct).to_csv('./ResultadosPY/Q3.csv', index=False)

# Exibindo formatado
print(pd.DataFrame(data_struct))


#Ambos os livros definem uma iteração como um passo num processo repetitivo onde a aproximação atual xk​ é usada para calcular uma nova aproximação x k+1​ , gerando uma sequência {xk​} que esperamos convergir para a solução exata α.
import matplotlib.pyplot as plt

# Aqui importaremos os vetores B, F e suas respectivas coordenadas de erros para criar gráficos de convergência. O gráfico mostrará o erro absoluto em função do número de iterações para cada método e cada tipo de precisão.
#Bisseção:  


plt.figure(figsize=(10, 6))

# Nomes para as legendas
labels = ['Float64 (Normal)', 'Float32 (Reduzida)', 'Truncamento (4 casas)']
cores = ['#2ecc71', '#3498db', '#e74c3c'] # Cores para cada linha do gráfico

# Lê os vetores em trios de dados para 3 coordenadas

for i in range(3):
    # B[x][y] e, que x define o qual dos trios de cooordenadas usaremos e y define qual coordenada do trio usaremos, no caso, a coordenada de erros (2) para plotar o gráfico de convergência.
    plt.plot(B[i][2], label=f'Bisseção - {labels[i]}', color=cores[i], linewidth=2)
    # i varia de 0 a 2, sendo 0 para float64, 1 para float32 e 2 para truncamento.

plt.yscale('log') # Escala logarítmica para ver a precisão melhor, já que os erros podem variar em ordens de magnitude.
plt.xlabel('Número de Iterações')
plt.ylabel('Erro Absoluto |x - ln(2)|')
plt.title('Impacto da Precisão na Convergência (Bisseção)')
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.savefig('./ResultadosPY/3.png', dpi=300)
plt.show()


#Grafico de convergencia para Falsa Posição:

plt.figure(figsize=(10, 6))
for i in range(3):
    plt.plot(F[i][2], label=f'Falsa Posição - {labels[i]}', color=cores[i], linewidth=2)
plt.yscale('log')
plt.xlabel('Número de Iterações')
plt.ylabel('Erro Absoluto |x - ln(2)|')
plt.title('Impacto da Precisão na Convergência (Falsa Posição)')
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.savefig('./ResultadosPY/3.1.png', dpi=300)
plt.show()


# Referência:
# [1] QUARTERONI, Alfio; SALERI, Fausto. Scientific computing with MATLAB and Octave. 2. ed. Berlin: Springer, 2006. (Texts in computational science and engineering, 2).
# [2] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.