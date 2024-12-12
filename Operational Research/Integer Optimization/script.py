from networkx import Graph, draw, get_node_attributes
from numpy import array, argwhere
from pulp import LpProblem, LpVariable, LpMaximize, lpSum
from matplotlib.pyplot import figure, text, savefig, show, title, gca
from os import makedirs

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
    try:
        with open(filename, 'r') as file:
            return array([list(map(float, linha.split())) for linha in file])
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return []

def create_graph(A: array, positions: array, solution: list, happiness: int):
    graph = Graph()
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

    idx = argwhere(A == 1.0)
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

    pos = get_node_attributes(graph, 'pos')
    edge_colors = [graph[u][v]['color'] for u, v in graph.edges()]

    return graph, profit, happiness, pos, edge_colors, node_colors

def plot_graph(graph: Graph, position: array, node_colors: list, edge_colors: list, total_cost: int, inhabitants: int, happiness: int, profit: int, output_filename="results/graph.png"):
    figure(figsize=(8, 8))
    draw(graph, position, with_labels=True, node_size=105, node_color=node_colors, font_size=6, font_weight='bold', edge_color=edge_colors)
    title("Grafo do Problema de Otimização")
    
    legend_text = f"Custo Total: {total_cost}\nHabitantes: {inhabitants}\nFelicidade: {happiness}\nLucro: {profit}"
    text(0.95, 0.05, legend_text, horizontalalignment='right', transform=gca().transAxes, fontsize=10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

    savefig(output_filename)
    show()

if __name__ == "__main__":
    MATRIX_FILENAME = 'problem.txt'
    POSITIONS_FILENAME = 'positions.txt'
    OUTPUT_FILENAME = 'results/solution.txt' 
    
    A = array(read_matrix_from_file(MATRIX_FILENAME))
    positions = array(read_matrix_from_file(POSITIONS_FILENAME))
    N = len(A) 
    happiness = 0
    inhabitants = 0
    total_cost = 0

    model = LpProblem("Plano Diretor da Cidade", LpMaximize)

    x_C, x_P, x_F, z_CP, z_CF, z_PF = create_binary_vars(N)

    L = lpSum((z_CF * A).flatten())
    inner_sum = [ [z_CP[i][j] - z_PF[i][j] for j in range(N) if A[i][j]] for i in range(N)]
    F = lpSum(x_P[i] - x_F[i] + lpSum(inner_sum[i]) for i in range(N))
    model += (2 * N ** 2 + 1) * L + F

    for i in range(N):
        model += x_C[i] + x_P[i] + x_F[i] == 1.0
        if i == 0:
            model += x_C[i] == 1.0  # Vértice 1 deve ser uma Casa
        for j in range(N):
            if A[i][j] == 1.0:
                model += x_C[i] + x_F[j] - 1 <= z_CF[i][j]
                model += x_C[i] >= z_CF[i][j]
                model += x_F[j] >= z_CF[i][j]

                model += x_C[i] + x_P[j] - 1 <= z_CP[i][j]
                model += x_C[i] >= z_CP[i][j]
                model += x_P[j] >= z_CP[i][j]

                model += x_P[i] + x_F[j] - 1 <= z_PF[i][j]
                model += x_P[i] >= z_PF[i][j]
                model += x_F[j] >= z_PF[i][j]

    model += F >= 0
    model += L >= 0

    model.solve()

solution = {}
for i in range(N):
    if x_C[i].varValue == 1.0:
        solution[i] = "Casa"
        total_cost += VERTEX_COSTS["Casa"]
        inhabitants += 1
    elif x_P[i].varValue == 1.0:
        solution[i] = "Parque"
        total_cost += VERTEX_COSTS["Parque"]
        happiness += 1
    elif x_F[i].varValue == 1.0:
        solution[i] = "Fábrica"
        total_cost += VERTEX_COSTS["Fábrica"]
        happiness += -1

graph, profit, happiness, pos, edge_colors, node_colors = create_graph(
    A, positions, [solution[i] for i in range(N)], happiness
)

makedirs('results', exist_ok=True)
plot_graph(graph, pos, node_colors, edge_colors, total_cost, inhabitants, happiness, profit)

try:
    with open(OUTPUT_FILENAME, 'w') as file:
        file.write("Solucao Otima:\n")
        for node, structure in solution.items():
            file.write(f"Vertice {node + 1}: {structure}\n")
        file.write(f"\nCusto Total: {total_cost}\n")
        file.write(f"Numero de Habitantes: {inhabitants}\n")
        file.write(f"Nivel de Felicidade: {happiness}\n")
        file.write(f"Lucro Total: {profit}\n")    
        file.write(f"Valor de L: {L.value()}\n")
        file.write(f"Valor de F: {F.value()}\n")
    print(f"Solução salva em '{OUTPUT_FILENAME}'.")
except Exception as e:
    print(f"Erro ao salvar a solução: {e}")
