from numpy import array, argwhere
from pulp import LpProblem, LpVariable, LpMaximize, lpSum
import networkx as nx
import matplotlib.pyplot as plt

VERTEX_COSTS = {
    "Casa": 25600,
    "Parque": 12800,
    "Fábrica": 19200
}

def create_binary_vars(N: int):
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

def read_matrix_from_file(filename: str):
    matrix = []
    try:
        with open(filename, 'r') as file:
            return array([list(map(float, linha.split())) for linha in file])
    except Exception as e:
        print(f"Erro ler arquivo: {e}")

    return matrix

def create_graph(A, positions, solution, happiness):
    graph = nx.Graph()
    profit = 0

    node_colors = []
    for i in range(len(A)):
        if solution[i] == 'Casa':
            node_colors.append('gray')  # Casa: cinza
        elif solution[i] == 'Fábrica':
            node_colors.append('blue')  # Fábrica: azul
        else:
            node_colors.append('green')  # Parque: verde
    
    for i in range(len(A)):
        graph.add_node(i, pos=positions[i])

    idx = argwhere(A == 1)
    for i, j in idx:
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
            edge_color = 'gray'
        graph.add_edge(i, j, color=edge_color)

    pos = nx.get_node_attributes(graph, 'pos')
    edge_colors = [graph[u][v]['color'] for u, v in graph.edges()]

    return graph, profit, happiness, pos, edge_colors, node_colors

def plot_graph(graph, position, node_colors, edge_colors, output_filename="graph.png"):
    plt.figure(figsize=(10, 10))
    nx.draw(graph, position, with_labels=True, node_size=175, node_color=node_colors, font_size=8, font_weight='bold', edge_color=edge_colors)
    plt.title("Grafo do Problema de Otimização")
    plt.savefig(output_filename)
    plt.show()

if __name__ == "__main__":
    MATRIX_FILENAME = 'problem.txt'
    POSITIONS_FILENAME = 'positions.txt'
    OUTPUT_FILENAME = 'solution.txt' 
    
    A = array(read_matrix_from_file(MATRIX_FILENAME))
    positions = array(read_matrix_from_file(POSITIONS_FILENAME))
    N = len(A) 
    happiness = 0
    inhabitants = 0
    total_cost = 0

    # Problema
    model = LpProblem("Plano Diretor da Cidade", LpMaximize)

    x_C, x_P, x_F, z_CP, z_CF, z_PF = create_binary_vars(N)

    # Função objetivo
    L = lpSum(z_CF[i][j] * A[i][j] for i in range(N) for j in range(N))
    F = lpSum(
        x_P[i] - x_F[i] + lpSum(z_CP[i][j] - z_PF[i][j] for j in range(N) if A[i][j])
        for i in range(N)
    )

    model += (2 * N ** 2 + 1) * L + F

    # Restrições
    for i in range(N):
        model += x_C[i] + x_P[i] + x_F[i] == 1
        if i == 0:
            model += x_C[i] == 1  # Vértice 1 deve ser uma Casa

        for j in range(N):
            if A[i][j]:
                model += x_C[i] + x_F[j] - 1 <= z_CF[i][j]
                model += x_C[i] >= z_CF[i][j]
                model += x_F[j] >= z_CF[i][j]

                model += x_C[i] + x_P[j] - 1 <= z_CP[i][j]
                model += x_C[i] >= z_CP[i][j]
                model += x_P[j] >= z_CP[i][j]

                model += x_P[i] + x_F[j] - 1 <= z_PF[i][j]
                model += x_P[i] >= z_PF[i][j]
                model += x_F[j] >= z_PF[i][j]

    for i in range(N): 
        for j in range(N): 
            if A[i][j] == 1.0: 
                model += z_CF[i][j] <= x_C[i]
                model += z_CF[i][j] <= x_F[j]
                model += z_CP[i][j] <= x_C[i]
                model += z_CP[i][j] <= x_P[j]
                model += z_PF[i][j] <= x_P[i]
                model += z_PF[i][j] <= x_F[j]
   
    model += F >= 0
    model += happiness >= 0

    model.solve()

    solution = []
    for i in range(N):
        if x_C[i].varValue == 1.0:
            solution.append("Casa")
            total_cost += VERTEX_COSTS["Casa"]
            inhabitants += 1
        elif x_P[i].varValue == 1.0:
            solution.append("Parque")
            total_cost += VERTEX_COSTS["Parque"]
            happiness += 1
        elif x_F[i].varValue == 1.0:
            solution.append("Fábrica")
            total_cost += VERTEX_COSTS["Fábrica"]
            happiness += -1

    graph, profit, happiness, pos, edge_colors, node_colors = create_graph(A, positions, solution, happiness)

    plot_graph(graph, pos, node_colors, edge_colors)

    try:
        with open(OUTPUT_FILENAME, 'w') as file:
            file.write("Solucao Otima:\n")
            for i, s in enumerate(solution):
                file.write(f"Vertice {i + 1}: {s}\n")
            file.write(f"\nCusto Total: {total_cost}\n")
            file.write(f"Numero de Habitantes: {inhabitants}\n")
            file.write(f"Nivel de Felicidade: {happiness}\n")
            file.write(f"Lucro Total: {profit}\n")
        print(f"Solução salva em '{OUTPUT_FILENAME}'.")
    except Exception as e:
        print(f"Erro ao salvar a solução: {e}")