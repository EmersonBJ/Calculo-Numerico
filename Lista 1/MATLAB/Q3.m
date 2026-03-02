% =========================================================================
% O Impacto dos Erros de Arredondamento na Busca de Raízes (Questão 3)
% =========================================================================
clear; clc; close all;

% Parâmetros Iniciais
raiz_exata = log(2); % Raiz analítica para comparação
a = -2; 
b = 2; 
t = 1e-16; % Tolerância

% =========================================================================
% EXECUÇÃO: Bisseção
% =========================================================================
[x_b64, it_b64, e_b64] = bissecao(a, b, t, 'float64', raiz_exata);
[x_b32, it_b32, e_b32] = bissecao(a, b, t, 'float32', raiz_exata);
[x_btr, it_btr, e_btr] = bissecao(a, b, t, 'trunc', raiz_exata);

fprintf('Bisseção com float64 - Raiz: %.15f | Iterações: %d\n', x_b64, it_b64);
fprintf('Bisseção com float32 - Raiz: %.15f | Iterações: %d\n', x_b32, it_b32);
fprintf('Bisseção com truncamento - Raiz: %.15f | Iterações: %d\n\n', x_btr, it_btr);

% =========================================================================
% EXECUÇÃO: Falsa Posição
% =========================================================================
[x_f64, it_f64, e_f64] = falsa_posicao(a, b, t, 'float64', raiz_exata);
[x_f32, it_f32, e_f32] = falsa_posicao(a, b, t, 'float32', raiz_exata);
[x_ftr, it_ftr, e_ftr] = falsa_posicao(a, b, t, 'trunc', raiz_exata);

fprintf('Falsa Posição com float64 - Raiz: %.15f | Iterações: %d\n', x_f64, it_f64);
fprintf('Falsa Posição com float32 - Raiz: %.15f | Iterações: %d\n', x_f32, it_f32);
fprintf('Falsa Posição com truncamento - Raiz: %.15f | Iterações: %d\n\n', x_ftr, it_ftr);

% =========================================================================
% TABELA DE DADOS (Equivalente ao Pandas DataFrame)
% =========================================================================
Metodo = {'Bisseção'; 'Bisseção'; 'Bisseção'; 'Falsa Posição'; 'Falsa Posição'; 'Falsa Posição'};
Modo = {'Float64'; 'Float32'; 'Truncamento'; 'Float64'; 'Float32'; 'Truncamento'};
Raiz_Final = [x_b64; x_b32; x_btr; x_f64; x_f32; x_ftr];
Iteracoes = [it_b64; it_b32; it_btr; it_f64; it_f32; it_ftr];
Erro_Final = [e_b64(end); e_b32(end); e_btr(end); e_f64(end); e_f32(end); e_ftr(end)];

TabelaResultados = table(Metodo, Modo, Raiz_Final, Iteracoes, Erro_Final);
disp(TabelaResultados);

% Salvando em CSV
if ~exist('ResultadosMAT', 'dir')
    mkdir('ResultadosMAT');
end
writetable(TabelaResultados, './ResultadosMAT/resultadosQ3.csv');
fprintf('Resultados salvos em ./ResultadosMAT/resultadosQ3.csv\n\n');

% =========================================================================
% GRÁFICOS DE CONVERGÊNCIA
% =========================================================================
figure('Name', 'Impacto da Precisão', 'Position', [100, 100, 800, 500]);

% Gráfico logarítmico (semilogy)
semilogy(1:it_b64, e_b64, 'Color', '#2ecc71', 'LineWidth', 2, 'DisplayName', 'Bisseção - Float64 (Normal)');
hold on; % Equivalente ao manter o gráfico aberto para adicionar mais linhas
semilogy(1:it_b32, e_b32, 'Color', '#3498db', 'LineWidth', 2, 'DisplayName', 'Bisseção - Float32 (Reduzida)');
semilogy(1:it_btr, e_btr, 'Color', '#e74c3c', 'LineWidth', 2, 'DisplayName', 'Bisseção - Truncamento (4 casas)');

xlabel('Número de Iterações');
ylabel('Erro Absoluto |x - ln(2)|');
title('Impacto da Precisão na Convergência (Bisseção)');
legend('show', 'Location', 'northeast');
grid on;

% =========================================================================
% FUNÇÕES LOCAIS (Devem ficar no final do script MATLAB)
% =========================================================================

% Função Principal com controle de precisão
function res = f_func(x, mode)
    val = exp(x) - 2;
    if strcmp(mode, 'trunc')
        res = fix(val * 1e4) / 1e4; % Simula o math.trunc do Python para 4 casas
    elseif strcmp(mode, 'float32')
        res = double(single(val)); % Força a perda de precisão e devolve pra double pra evitar conflito de matriz
    else
        res = val;
    end
end

% Método da Bisseção
function [x_final, it, e] = bissecao(a, b, tol, mode, raiz)
    it = 0;
    e = [];
    
    while abs(b - a) > tol && it < 100
        x = (a + b) / 2;
        it = it + 1;
        
        % Simulação de erro na variável calculada
        if strcmp(mode, 'trunc')
            x = fix(x * 1e4) / 1e4;
        elseif strcmp(mode, 'float32')
            x = double(single(x));
        end
        
        e(end+1) = abs(x - raiz); % Anexa o erro no array
        
        if f_func(x, mode) == 0
            break;
        elseif f_func(a, mode) * f_func(x, mode) < 0
            b = x;
        else
            a = x;
        end
    end
    x_final = x;
end

% Método da Falsa Posição
function [x_final, it, e] = falsa_posicao(a, b, tol, mode, raiz)
    it = 0;
    x = a;
    e = [];
    
    while abs(b - a) > tol && it < 100
        it = it + 1;
        
        % Trava de segurança contra divisão por zero
        den = f_func(b, mode) - f_func(a, mode);
        if den == 0
            break;
        end
        
        p = (a * f_func(b, mode) - b * f_func(a, mode)) / den;
        
        % Simulação de erro na variável calculada
        if strcmp(mode, 'trunc')
            p = fix(p * 1e4) / 1e4;
        elseif strcmp(mode, 'float32')
            p = double(single(p));
        end
        
        e(end+1) = abs(p - raiz);
        
        if f_func(p, mode) == 0
            x = p;
            break;
        end
        
        if f_func(a, mode) * f_func(p, mode) < 0
            b = p;
        else
            a = p;
        end
        x = p;
    end
    x_final = x;
end