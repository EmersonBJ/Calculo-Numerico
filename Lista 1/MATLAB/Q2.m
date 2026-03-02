% 1. O "Intervalo de Ouro" para ver a curva perfeitamente
X = linspace(0, 2, 1000);

% 2. O seu polinômio expandido
Y = X.^7 - 7*X.^6 + 21*X.^5 - 35*X.^4 + 35*X.^3 - 21*X.^2 + 7*X - 1;

% 3. Desenhando a linha
plot(X, Y, 'LineWidth', 2.5);

title('Visão Macro: Gráfico de f(x)');
xlabel('x');
ylabel('f(x)');
grid on;

% Linhas de referência cruzando exatamente no meio da curva
yline(0, 'k-', 'LineWidth', 1.5); 
xline(1, 'r--', 'LineWidth', 1.5);