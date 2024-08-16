from scipy.optimize import linprog

c = [8.99, 7.77, 25.98]  # Custos

A = [
    [-136, -80, 0],   # Carboidratos
    [-5, -2, -67],    # Gorduras Totais
    [-48, -13, -312], # Proteínas
    [-760, -3640, -1940] # Calorias
]

b = [-300, -55, -56, -2200]

result = linprog(c, A_ub=A, b_ub=b, method='simplex')

if result.success:
    print(f"Quantidade ótima de feijão (kg): {result.x[0]:.2f}")
    print(f"Quantidade ótima de arroz (kg): {result.x[1]:.2f}")
    print(f"Quantidade ótima de carne (kg): {result.x[2]:.2f}")
    print(f"Custo total: R$ {result.fun:.2f}")
else:
    print("Não foi possível encontrar uma solução ótima.")
