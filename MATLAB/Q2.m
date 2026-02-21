
Dist = ((1 + (2*10^-8)) - (1 - (2*10^-8))) / 400;
X = (1 - (2*10^-8)) : Dist : (1 + (2*10^-8));
Y = X.^7 - 7*X.^6 + 21*X.^5 - 35*X.^4 + 35*X.^3 - 21*X.^2 + 7*X - 1;


plot(X, Y);
title('Gráfico de f(x) no intervalo [1 - 2e-8, 1 + 2e-8]');
xlabel('x');
ylabel('f(x)');
grid on;


yline(0, 'k', 'LineWidth', 1.5); 
xline(1, 'r--', 'LineWidth', 1.2); 