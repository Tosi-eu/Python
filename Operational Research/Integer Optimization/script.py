from numpy import array, flatten
from pulp import LpProblem, LpVariable, LpMaximize, lpSum
import networkx as nx
import matplotlib.pyplot as plt

NOME_ARQUIVO_MATRIZ = 'problem.txt'

NOME_ARQUIVO_POSICOES = 'positions.txt'

CUSTOS_VERTICES = {
    "Casa": 25600,
    "Parque": 12800,
    "Fábrica": 19200
}

def createVars(N: int):
    try:
        x_C = array([LpVariable(f"x_C_{i}", cat="Binary") for i in range(N)])
        x_P = array([LpVariable(f"x_P_{i}", cat="Binary") for i in range(N)])
        x_F = array([LpVariable(f"x_F_{i}", cat="Binary") for i in range(N)])
        z_CP = array([[LpVariable(f"z_CP_{i}_{j}", cat="Binary") for j in range(N)] for i in range(N)])
        z_CF = array([[LpVariable(f"z_CF_{i}_{j}", cat="Binary") for j in range(N)] for i in range(N)])
        z_PF = array([[LpVariable(f"z_PF_{i}_{j}", cat="Binary") for j in range(N)] for i in range(N)])
    except Exception as e:
        print(f"Erro ao definir variáveis: {e}")

    return  x_C, x_P, x_F, z_CP, z_CF, z_PF

def ler_matriz_de_arquivo(nome_arquivo):
    matriz = []
    try:
        with open(nome_arquivo, 'r') as file:
                return [list(map(float, linha.split())) for linha in file]
    except Exception as e:
        print(f"Erro ler arquivo: {e}")

    return matriz

def get_node_colors(solution):
    node_colors = []
    for i in range(len(A)):
        if solution[i] == 'Casa':
            node_colors.append('gray')  # Casa: cinza
        elif solution[i] == 'Fábrica':
            node_colors.append('blue')  # Fábrica: azul
        else:
            node_colors.append('green')  # Parque: verde

    return node_colors

def create_graph(A, positions, solution, happiness):
    G = nx.Graph()
    profit = 0

    node_colors = get_node_colors(solution)

    for i in range(len(A)):
        G.add_node(i, pos=positions[i])

    for i in range(len(A)):
        for j in range(len(A)):
            if A[i][j] == 1:
                if (solution[i] == "Casa" and solution[j] == "Parque") or (solution[i] == "Parque" and solution[j] == "Casa"):
                    edge_color = 'green'  # Casa - Parque: verde
                    happiness += 1
                elif (solution[i] == "Casa" and solution[j] == "Fábrica") or (solution[i] == "Fábrica" and solution[j] == "Casa"):
                    edge_color = 'blue'  # Casa - Fábrica: azul
                    profit += 1
                elif (solution[i] == "Parque" and solution[j] == "Fábrica") or (solution[i] == "Fábrica" and solution[j] == "Parque"):
                    edge_color = 'red'  # Parque - Fábrica: vermelha
                    happiness += -1
                else:
                    edge_color = "gray"
                
                G.add_edge(i, j, color=edge_color)

    pos = nx.get_node_attributes(G, 'pos')
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]

    return profit, happiness, G, pos, node_colors, edge_colors

def plot_graph(graph, positions, node_colors, edge_colors):
    plt.figure(figsize=(10, 10))
    nx.draw(graph, positions, with_labels=True, node_size=250, node_color=node_colors, font_size=8, font_weight='bold', edge_color=edge_colors)
    plt.title("Grafo do Problema de Otimização")
    plt.show()

def get_solutions(N, x_C, x_P, x_F):
    total_cost = 0
    inhabitants = 0
    happiness = 0

    solution = []
    for i in range(N):
        if x_C[i].varValue == 1.0:
            solution.append("Casa")
            total_cost += CUSTOS_VERTICES["Casa"]
            inhabitants += 1
        elif x_P[i].varValue == 1.0:
            solution.append("Parque")
            total_cost += CUSTOS_VERTICES["Parque"]
            happiness += 1
        elif x_F[i].varValue == 1.0:
            solution.append("Fábrica")
            total_cost += CUSTOS_VERTICES["Fábrica"]
            happiness += -1

    return solution, total_cost, inhabitants, happiness

if __name__ == "__main__":
    A = array(ler_matriz_de_arquivo(NOME_ARQUIVO_MATRIZ))
    positions = array(ler_matriz_de_arquivo(NOME_ARQUIVO_POSICOES))
    N = len(A)
    happiness =0

    # Problema
    model = LpProblem("Plano Diretor da Cidade", LpMaximize)

    # Variáveis
    x_C, x_P, x_F, z_CP, z_CF, z_PF = createVars(N)

    # Função objetivo
    L = lpSum(z_CF[i][j] * A[i][j] for i in range(N) for j in range(N))
    F = lpSum(
        x_P[i] - x_F[i] + lpSum(z_CP[i][j] - z_PF[i][j] for j in range(N) if A[i][j])
        for i in range(N)
    )

    model += (2 * N ** 2 + 1) * L + F

    # Restrição das variáveis binárias
    for i in range(N):
        model += x_C[i] + x_P[i] + x_F[i] == 1
        if i == 0:
            model += x_C[i] == 1  # Vértice 1 deve ser uma Casa

        for j in range(N):
            if A[i][j]:
                # Verificações para z_CF (Casa-Fábrica), z_CP (Casa-Parque), e z_PF (Parque-Fábrica)
                model += z_CF[i][j] <= x_C[i], f"z_CF_cond1_{i}_{j}"
                model += z_CF[i][j] <= x_F[j], f"z_CF_cond2_{i}_{j}"
                model += z_CF[i][j] >= x_C[i] + x_F[j] - 1, f"z_CF_cond3_{i}_{j}"

                model += z_CP[i][j] <= x_C[i], f"z_CP_cond1_{i}_{j}"
                model += z_CP[i][j] <= x_P[j], f"z_CP_cond2_{i}_{j}"
                model += z_CP[i][j] >= x_C[i] + x_P[j] - 1, f"z_CP_cond3_{i}_{j}"

                model += z_PF[i][j] <= x_P[i], f"z_PF_cond1_{i}_{j}"
                model += z_PF[i][j] <= x_F[j], f"z_PF_cond2_{i}_{j}"
                model += z_PF[i][j] >= x_P[i] + x_F[j] - 1, f"z_PF_cond3_{i}_{j}"

    # Restrições de poda: verificações adicionais
    for i in range(N):
        for j in range(N):
            if A[i][j] == 1.0: 
                model += z_CF[i][j] <= x_C[i]
                model += z_CF[i][j] <= x_F[j]
                model += z_CP[i][j] <= x_C[i]
                model += z_CP[i][j] <= x_P[j]
                model += z_PF[i][j] <= x_P[i]
                model += z_PF[i][j] <= x_F[j]
    
    # Poda de happineess e profit (não precisa ser negativa)
    model += F >= 0
    model += happiness >= 0

    model.solve()

    # Verificar solução
    solution, total_cost, inhabitants, happiness = get_solutions(N, x_C, x_P, x_F)

    # Plotar o grafo com as cores
    profit, happiness, G, pos, node_colors, edge_colors = create_graph(A, positions, solution, happiness)

    plot_graph(G, pos, node_colors, edge_colors)
  
    print(f"Lucro: {profit}")
    print(f"Felicidade: {happiness}")
    print(f"Custo Total: {total_cost}")
    print(f"Habitantes: {inhabitants}")
