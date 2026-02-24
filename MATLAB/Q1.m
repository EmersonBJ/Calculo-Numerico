clear; clc;

% 1. Mostrando os Limites da Máquina
fprintf('--- LIMITES DA MÁQUINA (MATLAB) ---\n');
fprintf('Maior número flutuante (realmax): %e\n', realmax);
fprintf('Menor número flutuante (realmin): %e\n', realmin);
fprintf('Epsilon da máquina (eps):         %e\n\n', eps);

% 2. Avaliação de Erros da Expressão f(x) = ((1 + x) - 1) / x
v_exato = 1.0; % Matematicamente, o resultado deveria ser sempre 1
x_vals = [1e-15, 1e15];

fprintf('--- AVALIAÇÃO DOS ERROS ---\n');
for i = 1:length(x_vals)
    x = x_vals(i);
    
    % Cálculo da função
    f_x = ((1.0 + x) - 1.0) / x;
    
    % Cálculo dos erros
    erro_abs = abs(v_exato - f_x);
    erro_rel = erro_abs / abs(v_exato);
    
    % Exibição
    fprintf('Para x = %g:\n', x);
    fprintf('  Resultado calculado : %1.15f\n', f_x);
    fprintf('  Erro Absoluto       : %e\n', erro_abs);
    fprintf('  Erro Relativo       : %e\n\n', erro_rel);
end
