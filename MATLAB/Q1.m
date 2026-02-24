fprintf('Maior número flutuante (realmax): %e\n', realmax);
fprintf('Menor número flutuante (realmin): %e\n', realmin);
fprintf('Epsilon da máquina (eps): %e\n', eps);

v= 1.0; %Valor exato da funcao
a = [1e-15, 1e15]; %intervalo de texte

for i = 1:length(a)
    x = a(i);
   
    f_x = ((1.0 + x) - 1.0) / x;
    
    erro_absoluto = abs(v - f_x);
    erro_relativo = erro_absoluto / abs(v);
    
    fprintf('  Valor calculado: %1.15f\n', f_x);
    fprintf('  Erro Absoluto:   %e\n', erro_absoluto);
    fprintf('  Erro Relativo:   %e\n\n', erro_relativo);
end
