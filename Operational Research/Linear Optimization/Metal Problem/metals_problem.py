from scipy.optimize import linprog

c = [20, 25, 30]  # Custos

A = [
    [-0.50, -0.30, -0.20],   # Alumínio (deve ser pelo menos 30%)
    [-0.30, -0.50, -0.60],   # Cobre (deve ser pelo menos 40%)
    [-0.20, -0.20, -0.20],   # Zinco (deve ser exatamente 20%)
    [1, 1, 1]                # Peso total deve ser 100 kg
]

# Valores das restrições
b = [-0.30, -0.40, -0.20, 100]

result = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None)]*3, method='simplex')

# Exibir resultados
if result.success:
    print(f"Quantidade ótima de Metal A (kg): {result.x[0]:.2f}")
    print(f"Quantidade ótima de Metal B (kg): {result.x[1]:.2f}")
    print(f"Quantidade ótima de Metal C (kg): {result.x[2]:.2f}")
    print(f"Custo total: R$ {result.fun:.2f}")
else:
    print("Não foi possível encontrar uma solução ótima.")
