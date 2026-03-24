# Question 1.
# Encontre a raiz da função y(x) dada pelos pontos abaixo:
# X:    0      | 0.5    | 1      | 1.5    | 2      | 2.5     | 3      
# y(x): 1.8421 | 2.4694 | 2.4921 | 1.9047 | 0.8509 | -0.4112 | -1.5727
# Use interpolação de Lagrange sobre (a) três e (b) quatro pontos consecutivos.

# -----------------------------------------------------------------------------------------
# Interpolacao inversa: em vez de y(x)=0, achamos x(0). Calculamos x em funcao de y.
# [1] Cap 3.2 - Interpolacao de Lagrange
def lagrange_inverso(pontos, valor_y_alvo):
    raiz_x = 0.0
    
    # iterando sobre cada ponto pra montar o polinomio
    for i in range(len(pontos)):
        Li = 1.0 # termo multiplicador de lagrange pra esse ponto
        
        for j in range(len(pontos)):
            if i != j:
                # monta a fracao: produtorio de (y - y_j) / (y_i - y_j)
                Li *= (valor_y_alvo - pontos[j][1]) / (pontos[i][1] - pontos[j][1])
        
        # soma o parcelamento atual na raiz
        raiz_x += pontos[i][0] * Li
        
    return raiz_x


if __name__ == "__main__":
    print("Resultados da Interpolacao Inversa de Lagrange:")
    
    # a raiz ta entre 2 (y positivo) e 2.5 (y negativo), pegando os mais proximos
    
    # (a) 3 pontos consecutivos proximos do 0 alvo
    p3 = [[1.5, 1.9047], [2, 0.8509], [2.5, -0.4112]]
    raiz_3 = lagrange_inverso(p3, 0.0)
    print(f"(a) Raiz estimada com 3 pontos: {raiz_3:.6f}")
    
    # (b) 4 pontos consecutivos proximos do 0 alvo pra maior precisao
    p4 = [[1.5, 1.9047], [2, 0.8509], [2.5, -0.4112], [3, -1.5727]]
    raiz_4 = lagrange_inverso(p4, 0.0)
    print(f"(b) Raiz estimada com 4 pontos: {raiz_4:.6f}")

# Referencias:
# [1] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.

# Referência:
# [1] BURDEN, Richard L.; FAIRES, J. Douglas. Numerical analysis. 9. ed. Boston: Brooks/Cole; Cengage Learning, 2011.