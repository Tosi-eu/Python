from pprint import pprint
import numpy as np
from pulp import LpProblem, LpVariable, LpMaximize, lpSum
import networkx as nx
import matplotlib.pyplot as plt

habitantes = 0
felicidade = 0
custo = 0

# Custos dos vértices
custos_vertices = {
    "Casa": 25600,
    "Parque": 12800,
    "Fábrica": 19200
}

# Função para ler matriz de arquivo
def ler_matriz_de_arquivo(nome_arquivo):
    matriz = []
    try:
        with open(nome_arquivo, 'r') as file:
            for linha in file:
                # Divide cada linha em valores e converte para inteiros
                valores = list(map(int, linha.split()))
                matriz.append(valores)
    except ValueError as _:
        with open(nome_arquivo, 'r') as file:
            for linha in file:
                # Divide cada linha em valores e converte para float
                valores = list(map(float, linha.split()))
                matriz.append(valores)
    except Exception as e:
        print(f"Erro ler arquivo: {e}")

    return matriz

def plotar_grafo(A, positions, solution, felicidade=felicidade):
    G = nx.Graph()
    lucro = 0

    node_colors = []
    for i in range(len(A)):
        if solution[i] == 'Casa':
            node_colors.append('gray')  # Casa: cinza
        elif solution[i] == 'Fábrica':
            node_colors.append('blue')  # Fábrica: azul
        else:
            node_colors.append('green')  # Parque: verde
    
    # Adicionar nós e arestas de acordo com a matriz A
    for i in range(len(A)):
        G.add_node(i, pos=positions[i])

    for i in range(len(A)):
        for j in range(len(A)):
            edge_color = "gray"
            if A[i][j] == 1:
                if (solution[i] == "Casa" and solution[j] == "Parque") or (solution[i] == "Parque" and solution[j] == "Casa"):
                    edge_color = 'green'  # Casa - Parque: verde
                    felicidade += 1
                if (solution[i] == "Casa" and solution[j] == "Fábrica") or (solution[i] == "Fábrica" and solution[j] == "Casa"):
                    edge_color = 'blue'  # Casa - Fábrica: azul
                    lucro += 1
                if (solution[i] == "Parque" and solution[j] == "Fábrica") or (solution[i] == "Fábrica" and solution[j] == "Parque"):
                    edge_color = 'red'  # Parque - Fábrica: vermelha
                    felicidade += -1
                G.add_edge(i, j, color=edge_color)

    # Plotar o grafo com as cores
    pos = nx.get_node_attributes(G, 'pos')
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]
    
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_size=250, node_color=node_colors, font_size=8, font_weight='bold', edge_color=edge_colors)
    plt.title("Grafo do Problema de Otimização")
    plt.show()

    return lucro, felicidade


if __name__ == "__main__":
    # Ler matriz do arquivo
    NOME_ARQUIVO_MATRIZ = 'problem.txt'
    NOME_ARQUIVO_POSICOES = 'positions.txt'

    A = np.array(ler_matriz_de_arquivo(NOME_ARQUIVO_MATRIZ))
    positions = np.array(ler_matriz_de_arquivo(NOME_ARQUIVO_POSICOES))
    N = len(A)  # Número de vértices no grafo

    # Problema
    model = LpProblem("Plano Diretor da Cidade", LpMaximize)

    # Variáveis
    x_C = [LpVariable(f"x_C_{i}", cat="Binary") for i in range(N)]
    x_P = [LpVariable(f"x_P_{i}", cat="Binary") for i in range(N)]
    x_F = [LpVariable(f"x_F_{i}", cat="Binary") for i in range(N)]
    z_CP = [[LpVariable(f"z_CP_{i}_{j}", cat="Binary") for j in range(N)] for i in range(N)]
    z_CF = [[LpVariable(f"z_CF_{i}_{j}", cat="Binary") for j in range(N)] for i in range(N)]
    z_PF = [[LpVariable(f"z_PF_{i}_{j}", cat="Binary") for j in range(N)] for i in range(N)]

    # Função objetivo
    L = lpSum(z_CF[i][j] * A[i][j] for i in range(N) for j in range(N))
    F = lpSum(
        x_P[i] - x_F[i] + lpSum(z_CP[i][j] - z_PF[i][j] for j in range(N) if A[i][j])
        for i in range(N)
    )

    model += (2 * N ** 2 + 1) * L + F

    # Restrições
    for i in range(N):
        # Cada vértice tem uma estrutura (Casa, Parque, ou Fábrica)
        model += x_C[i] + x_P[i] + x_F[i] == 1
        if i == 0:
            model += x_C[i] == 1  # Vértice 1 deve ser uma Casa

        for j in range(N):
            if A[i][j]:
                # Linearização para z_CF
                model += x_C[i] + x_F[j] - 1 <= z_CF[i][j]
                model += x_C[i] >= z_CF[i][j]
                model += x_F[j] >= z_CF[i][j]

                # Linearização para z_CP
                model += x_C[i] + x_P[j] - 1 <= z_CP[i][j]
                model += x_C[i] >= z_CP[i][j]
                model += x_P[j] >= z_CP[i][j]

                # Linearização para z_PF
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

    model.solve()

    solution = []
    for i in range(N):
        if x_C[i].varValue == 1.0:
            solution.append("Casa")
            custo += custos_vertices["Casa"]
            habitantes += 1
        elif x_P[i].varValue == 1.0:
            solution.append("Parque")
            custo += custos_vertices["Parque"]
            felicidade += 1
        elif x_F[i].varValue == 1.0:
            solution.append("Fábrica")
            custo += custos_vertices["Fábrica"]
            felicidade += -1

    # Plotar o grafo com as cores
    lucro, felicidade = plotar_grafo(A, positions, solution)

    print("Solução: ", solution)    
    print(f"Lucro: {lucro}")
    print(f"Felicidade: {felicidade}")
    print(f"Custo Total: {custo}")
    print(f"Habitantes: {habitantes}")
