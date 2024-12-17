import os
import time
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

from numpy import array

def read_matrix_and_positions_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read().split("Positions:")
            
            matrix = array([[int(x) for x in line.split()] for line in data[0].strip().split("\n")[1:]])

            positions = [eval(line.split(':')[1]) for line in data[1].strip().split("\n")]

            return matrix, positions
    except Exception as e:
        print(e)
        exit(1)

def create_graph(A: array, positions: array, solution: list):
    graph = Graph()

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
        elif (solution[i] == "Casa" and solution[j] == "Fábrica") or (solution[i] == "Fábrica" and solution[j] == "Casa"):
            edge_color = 'blue'  # Casa - Fábrica: azul
        elif (solution[i] == "Parque" and solution[j] == "Fábrica") or (solution[i] == "Fábrica" and solution[j] == "Parque"):
            edge_color = 'red'  # Parque - Fábrica: vermelha
        else:
            edge_color = 'gray'
        graph.add_edge(i, j, color=edge_color)

    pos = get_node_attributes(graph, 'pos')
    edge_colors = [graph[u][v]['color'] for u, v in graph.edges()]

    return graph, pos, edge_colors, node_colors

def save_graph(A, graph: Graph, position: array, node_colors: list, edge_colors: list, total_cost: int, inhabitants: int, happiness: int, profit: int, output_plot_filename):
    figure(figsize=(8, 8))
    draw(graph, position, with_labels=True, labels={i: (i+1) for i in range(len(A))}, node_size=105, node_color=node_colors, font_size=6, font_weight='bold', edge_color=edge_colors)
    title("Grafo do Problema de Otimização")
    
    legend_text = f"Custo Total: {total_cost}\nHabitantes: {inhabitants}\nFelicidade: {happiness}\nLucro: {profit}"
    text(0.95, 0.05, legend_text, horizontalalignment='right', transform=gca().transAxes, fontsize=10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

    savefig(output_plot_filename)

def tabu_search(N, initial_solution, iterations=100000, tenure=10, max_no_improve=10):
    best_solution = initial_solution
    best_cost = calculate_cost(best_solution)
    tabu_list = [best_solution]
    current_solution = best_solution
    global_best_value = best_cost  
    no_improve_count = 0

    for _ in range(iterations):
        if no_improve_count == max_no_improve:
            break  

        neighbors = get_neighbors(current_solution, N)
        best_neighbor = None
        best_neighbor_cost = float('inf')

        for neighbor in neighbors:
            if neighbor not in tabu_list:
                neighbor_cost = calculate_cost(neighbor) 

                if neighbor_cost < best_neighbor_cost:
                    best_neighbor_cost = neighbor_cost
                    best_neighbor = neighbor
                    global_best_value = best_neighbor_cost
        
        if best_neighbor:
            local_neighbors = get_neighbors(best_neighbor, N)
            for local_neighbor in local_neighbors:
                local_cost = calculate_cost(local_neighbor)
                if local_cost < best_neighbor_cost:
                    best_neighbor = local_neighbor
                    best_neighbor_cost = local_cost

            current_solution = best_neighbor
            tabu_list.append(current_solution)
            if len(tabu_list) > tenure:
                tabu_list.pop(0)

        if best_neighbor_cost < best_cost and best_cost < global_best_value:
            best_cost = best_neighbor_cost
            best_solution = current_solution
            no_improve_count = 0 
        else:
            no_improve_count += 1

    return best_solution, best_cost

def calculate_cost(solution):
    total_cost = 0

    for i in range(len(solution)):
        if solution[i] == "Casa":
            total_cost += VERTEX_COSTS["Casa"]
        elif solution[i] == "Parque":
            total_cost += VERTEX_COSTS["Parque"]
        elif solution[i] == "Fábrica":
            total_cost += VERTEX_COSTS["Fábrica"]

    return total_cost

def get_neighbors(solution, N):
    neighbors = []
    for i in range(N):
        new_solution = solution[:]
        if solution[i] == "Casa":
            new_solution[i] = "Parque"
        elif solution[i] == "Parque":
            new_solution[i] = "Fábrica"
        else:
            new_solution[i] = "Casa"
        neighbors.append(new_solution)
    return neighbors

def optimize_and_save_graph(problem_file, output_graph_filename, output_txt_file, testing=False):
    folder = 'results/'
        
    if testing:
        makedirs('test_results', exist_ok=True)
        folder = 'test_results/'
    else:
        makedirs('results', exist_ok=True)

    start_time = time.time()

    A, positions = read_matrix_and_positions_from_file(problem_file)
    N = len(A)
    
    model = LpProblem("Plano Diretor da Cidade", LpMaximize)

    x_C, x_P, x_F, z_CP, z_CF, z_PF = create_binary_vars(N)

    L = lpSum(z_CF[i, j] * A[i][j] for i in range(N) for j in range(N))
    F = lpSum((x_P[i] - x_F[i] + lpSum((z_CP[i, j] - z_PF[i, j]) * A[i][j] for j in range(N))) for i in range(N))
    H = lpSum(x_C[i] for i in range(N))
    C = lpSum(x_C[i] * VERTEX_COSTS['Casa'] + x_F[i] * VERTEX_COSTS["Fábrica"] + x_P[i] * VERTEX_COSTS["Parque"] for i in range(N))
    
    model += (2 * N ** 2 + 1) * L + 1e-3 * F - 1e-9 * C + H * 1e-12

    for i in range(N):
        model += x_C[i] + x_P[i] + x_F[i] == 1
        for j in range(N):
            if A[i][j] == 1:
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
    model += x_C[0] == 1
    model.solve()

    solution = {}
    initial_solution = []
    for i in range(N):
        if x_C[i].varValue == 1:
            solution[i] = "Casa"
            initial_solution.append("Casa")
        elif x_F[i].varValue == 1:
            solution[i] = "Fábrica"
            initial_solution.append("Fábrica")
        elif x_P[i].varValue == 1:
            solution[i] = "Parque"
            initial_solution.append("Parque")

    tabu_solution, tabu_cost = tabu_search(N, initial_solution)

    if C.value() < tabu_cost:
        graph, pos, edge_colors, node_colors = create_graph(A, positions, solution)
        save_graph(A, graph, pos, node_colors, edge_colors, C.value(), int(H.value()), int(F.value()), int(L.value()), f'{folder}{output_graph_filename}')
    else:
        graph, pos, edge_colors, node_colors = create_graph(A, positions, tabu_solution)
        save_graph(A, graph, pos, node_colors, edge_colors, tabu_cost, int(H.value()), int(F.value()), int(L.value()), f'{folder}{output_graph_filename}')

    execution_time = time.time() - start_time

    try:
        with open(f'{folder}{output_txt_file}', 'w') as file:
            file.write("Solução Ótima do Modelo:\n")
            for i in range(N):
                file.write(f"Vértice {i+1}: {solution[i]}\n")
            file.write(f"\nMatriz de Adjacência: {A}\n")
            file.write(f"\nPosições: {positions}\n\n\n")
            file.write(f"\nCusto Total: {C.value()}\n")
            file.write(f"Habitantes: {int(H.value())}\n")
            file.write(f"Felicidade: {F.value()}\n")
            file.write(f"Lucro: {L.value()}\n")
            file.write(f"Tempo de Execução: {execution_time:.2f} segundos\n")
    except Exception as e:
        print(f"Erro ao salvar resultado: {e}")

def test_single_file(file_path, output_graph_filename, output_txt_filename, testing):

    if not os.path.exists(file_path):
        print(f"Arquivo não encontrado: {file_path}")
        return
    
    try:
        optimize_and_save_graph(file_path, output_graph_filename, output_txt_filename, testing=testing)
    except Exception as e:
        print(f"Erro ao testar o arquivo {file_path}: {e}")


if __name__ == "__main__":
    problems_folder = 'problems/'
    test_folder = 'test_problems/'

    single_test_file = 'problems/problem_1.txt'

    graph_output_file = 'single_problem_1_solved.png'
    txt_output_file = 'single_problem_1_solved.txt'

    test_single_file(single_test_file, graph_output_file, txt_output_file, False)
