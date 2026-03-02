% =========================================================================
% Competição de Métodos: Quem Encontra a Raiz Mais Rápido? (Questão 4)
% =========================================================================
% Objetivo: Comparar Ponto Fixo, Newton-Raphson e Secante.
% Função Escolhida: f(x) = x^3 - 7x + 6
%
% NOTA METODOLÓGICA (OVERHEAD CONSTANTE):
% O x final não é do interesse da tabela. Alguns dos métodos utilizados para 
% medir o erro a cada passo podem retardar o tempo absoluto de cada função. 
% No entanto, como aplicamos o mesmo overhead a todos, a comparação de tempo 
% continua justa e reflete perfeitamente a eficiência dos algoritmos!

clear; clc; close all;

% Parâmetros Iniciais
raizes = [1, 2, -3]; % Para comparação de erros
tol = 1e-5;

% =========================================================================
% EXECUÇÃO DOS MÉTODOS
% =========================================================================
[it_pf, e_pf, name_pf, t_pf] = ponto_fixo(0.5, tol, raizes);
[it_nw, e_nw, name_nw, t_nw] = newton(0.5, tol, raizes);
[it_sc, e_sc, name_sc, t_sc] = secante([0.5, 0.6], tol, raizes);

% Agrupando os resultados num "Cell Array" para podermos ordenar
R = {
    it_pf, e_pf, name_pf, t_pf;
    it_nw, e_nw, name_nw, t_nw;
    it_sc, e_sc, name_sc, t_sc
};

% Ordenando pelo número de iterações (Coluna 1)
R = sortrows(R, 1);

% =========================================================================
% TABELA DE DADOS E EXPORTAÇÃO
% =========================================================================
Posicao = [1; 2; 3];
Metodo = {R{1,3}; R{2,3}; R{3,3}};
Iteracoes = [R{1,1}; R{2,1}; R{3,1}];
Tempo_s = [R{1,4}; R{2,4}; R{3,4}];

% Extraindo o último erro da lista de cada método
erro1 = R{1,2}; erro2 = R{2,2}; erro3 = R{3,2};
Erro_Final = [erro1(end); erro2(end); erro3(end)];

% Criando e exibindo a Tabela
TabelaResultados = table(Posicao, Metodo, Iteracoes, Erro_Final, Tempo_s);
disp(' ');
disp('🏆 RANKING DE EFICIÊNCIA 🏆');
disp(TabelaResultados);

% Salvando em CSV
writetable(TabelaResultados, 'resultados_q4.csv');
fprintf('Resultados salvos em "resultados_q4.csv"\n\n');

% =========================================================================
% GRÁFICOS DE CONVERGÊNCIA
% =========================================================================
figure('Name', 'Competição de Convergência', 'Position', [100, 100, 800, 500]);

% Dicionário de cores no MATLAB
cores = containers.Map({'Ponto Fixo', 'Newton-Raphson', 'Secante'}, ...
                       {'#3498db', '#2ecc71', '#e74c3c'});

hold on; % Mantém o gráfico aberto para desenhar as 3 linhas juntas
for i = 1:3
    iter = R{i, 1};
    erros = R{i, 2};
    nome = R{i, 3};
    
    % semilogy já cria o eixo Y logarítmico direto
    semilogy(1:iter, erros, '-o', 'LineWidth', 2, ...
             'Color', cores(nome), 'DisplayName', nome);
end
hold off;

xlabel('Número de Iterações');
ylabel('Erro Absoluto |x_i - raiz|');
title('Competição de Convergência: f(x) = x^3 - 7x + 6');
legend('show');
grid on;


% =========================================================================
% FUNÇÕES LOCAIS (Devem ficar no final do script no MATLAB)
% =========================================================================

% Função Principal e Derivadas
function y = f(x)
    y = x^3 - 7*x + 6;
end

function y = df(x)
    y = 3*x^2 - 7;
end

function y = phi(x)
    y = (x^3 + 6) / 7;
end

% -------------------------------------------------------------------------
% 1. Método do Ponto Fixo
% -------------------------------------------------------------------------
function [it, e, name, tempo] = ponto_fixo(x0, t, raizes)
    name = 'Ponto Fixo';
    x = x0;
    e = [];
    it = 0;
    
    tic; % Inicia o cronômetro (perf_counter do MATLAB)
    while it < 100
        x_novo = phi(x(end));
        x(end+1) = x_novo;
        it = it + 1;
        
        e(end+1) = min(abs(x(end) - raizes));
        
        if abs(x(end) - x(end-1)) < t
            break;
        end
    end
    tempo = toc; % Para o cronômetro
end

% -------------------------------------------------------------------------
% 2. Método de Newton-Raphson
% -------------------------------------------------------------------------
function [it, e, name, tempo] = newton(x0, t, raizes)
    name = 'Newton-Raphson';
    x = x0;
    e = [];
    it = 0;
    
    tic;
    while it < 100
        derivada = df(x(end));
        if derivada == 0; break; end 
            
        x_novo = x(end) - f(x(end))/derivada;
        x(end+1) = x_novo;
        it = it + 1;
        
        e(end+1) = min(abs(x(end) - raizes));
        
        if abs(x(end) - x(end-1)) < t
            break;
        end
    end
    tempo = toc;
end

% -------------------------------------------------------------------------
% 3. Método da Secante
% -------------------------------------------------------------------------
function [it, e, name, tempo] = secante(x_arr, t, raizes)
    name = 'Secante';
    x = x_arr; % Recebe os 2 palpites iniciais
    e = [];
    it = 0; % Contador de NOVAS iterações
    
    tic;
    while it < 100
        denominador = f(x(end)) - f(x(end-1));
        if denominador == 0; break; end 
            
        novo_x = x(end) - (((x(end) - x(end-1)) * f(x(end))) / denominador);
        x(end+1) = novo_x;
        it = it + 1;
        
        e(end+1) = min(abs(x(end) - raizes));
        
        if abs(x(end) - x(end-1)) < t
            break;
        end
    end
    tempo = toc;
end