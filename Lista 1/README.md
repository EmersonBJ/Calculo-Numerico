Repositório da Lista 1 de Cálculo Numérico
Autores: Eduardo Fernández Britto, Emerson Wilson Branco Junior, Lucas Peracine de Oliveira Fabrino, Raphael Henrique Tavares da Silva.

​Questão 1: Limites Computacionais e Cancelamento Catastrófico
O objetivo desta etapa foi determinar as fronteiras de representação numérica do sistema operando sob o padrão de distribuição IEEE 754 de 64 bits.
​Limites de Representação: A variável realmax define o limite superior antes da ocorrência de overflow (1.79\times10^{308}), enquanto realmin define o limite numérico inferior para números normalizados antes da ocorrência de underflow (2.22\times10^{-308}).
​Épsilon da Máquina (eps): A precisão relativa do sistema é delimitada pelo épsilon da máquina, quantificado em aproximadamente 2.22\times10^{-16}.
​Avaliação do Erro Relativo: Na avaliação da expressão f(x)=\frac{(1+x)-1}{x}, cujo limite analítico corresponde a 1.0 para x\neq0, a aplicação da constante x=10^{-15} demonstra o fenômeno numérico de cancelamento catastrófico. A perda de dígitos significativos durante a subtração resulta em um erro relativo de magnitude aproximada de 11\%.
​
Questão 2: Erros de Arredondamento em Expansões Polinomiais
Avaliou-se o comportamento numérico iterativo da expansão binomial f(x)=x^7-7x^6+21x^5-35x^4+35x^3-21x^2+7x-1, (pelo triângulo de Pascal podemos reconhecer que é a função (x-1)⁷).
​Comportamento em Larga Escala: Em um intervalo de domínio amplo, a representação gráfica condiz satisfatoriamente com o modelo teórico contínuo, denotando a intersecção de raízes no ponto 1.
​Comportamento em Escala Microscópica: Em um intervalo de análise de ordem 10^{-8} em torno da raiz teórica, fomos capazes de ver a limitação imposta pela resoluçãoda maquina(x64). A realização de sucessivas subtrações de valores em grandeza escalar desproporcional gera ruído de arredondamento elevado, comprometendo a monotonicidade e estabilidade da curva.

​Questão 3: Convergência da Bisseção e Falsa Posição Sob a Precisão
Analisou-se a convergência da função f(x)=e^x-2 mediante o uso da Bisseção e da Falsa Posição. A implementação abordou de forma ativa a supressão de precisão escalar durante a execução temporal (float64, float32 e truncamento):
​Critério de Parada em Precisão Reduzida: Operando nativamente em precisão simples (float32), os métodos encerram suas iterações de forma prematura ao classificar o resíduo computacional como nulo. A verificação comparativa em base 64 bits revelou a estagnação do erro absoluto na ordem de 10^{-8}.
​Instabilidade Numérica da Falsa Posição: Constatou-se a acentuada sensibilidade da Falsa Posição à supressão de dígitos. Ao incutir um truncamento estático de 4 casas decimais, o denominador responsável pelo cálculo da secante perdeu sua significância, mantendo o método estático em laço iterativo restrito até o esgotamento do limite máximo de operações imposto pelo código. Em contrapartida, o método da Bisseção revelou-se analiticamente mais robusto.
​
Questão 4: Avaliação de Desempenho de Algoritmos Iterativos
Fizeemos uma avaliação comparativa de performance entre os métodos de Newton-Raphson, Secante e Ponto Fixo para a localização de raízes em funções não lineares.
​Eficiência: Conforme vimos no gráfico, o método de Newton-Raphson teve o melhor desempenho, exibindo a menor contagem de iterações e a menor dimensão de erro graças à sua taxa de convergência.
​
Questão 5: Pêndulo Simples
Procedeu-se extraindo o vetor angular inicial \theta necessário à padronização do pêndulo operando sob o período de 2.0 segundos.
​Escala: Os algoritmos convergem numericamente, usamos medições em radianos para evitar as perdas de ponto flutuante por constantes de conversão. O uso metodológico do arcosseno serve para restringir ao primeiro quadrante rm pontos positivos.
​Critério de Parada: Usamos a condição adicional (if c == a or c == b: break), afim de impedir no looping infinito nos objetos truncados.
