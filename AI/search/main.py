from time import time
import networkx as nx
from random import uniform, random
from math import exp, sqrt
import matplotlib.pyplot as plt

class Buscas:
    def __init__(self, quantidade_elementos, alcance_medio):
        self.quantidade_elementos = quantidade_elementos
        self.alcance_medio = alcance_medio
        self.lista_vertices, self.lista_arestas = self._gera_rede()
        self.grafo = nx.Graph()
        self.grafo.add_nodes_from(range(quantidade_elementos))
        self.grafo.add_weighted_edges_from(self.lista_arestas)
        self.pos = {i: self.lista_vertices[i] for i in range(self.quantidade_elementos)}

    def _media(self, lista):
        return sum(lista) / len(lista)

    def _gera_rede(self):
        lista_vertices = self._gera_vertices()
        lista_arestas = self._gera_arestas(lista_vertices)
        return lista_vertices, lista_arestas

    def _gera_vertices(self):
        lista_vertices = []
        for _ in range(self.quantidade_elementos):
            x = uniform(0, self.quantidade_elementos)
            y = uniform(0, self.quantidade_elementos)
            lista_vertices.append((x, y))
        return lista_vertices

    def _gera_arestas(self, lista_vertices):
        lista_arestas = []
        quantidade_elementos = len(lista_vertices)
        for i in range(quantidade_elementos):
            for j in range(i + 1, quantidade_elementos):
                x1, y1 = lista_vertices[i]
                x2, y2 = lista_vertices[j]
                distancia_euclidiana = sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))
                probabilidade = exp(-self.alcance_medio * distancia_euclidiana) #de criar uma aresta entre vértices
                if random() < probabilidade:
                    lista_arestas.append((i, j, distancia_euclidiana))
        return lista_arestas
    
    def plotar_grafico(self):
        nx.draw_networkx(self.grafo, pos=self.pos, with_labels=False, node_size=1)
        plt.show()

    def plotar_caminho_gerado(self, metodo):
        for i in metodo:
            if i is None:
                metodo.remove(i)

        caminho = metodo
        print("Caminho percorrido:", caminho if caminho is not None else "Não há caminho entre a origem e o destino.")

        arestas_percorridas = [(caminho[i], caminho[i+1]) for i in range(len(caminho)-1)]
        nx.draw_networkx(self.grafo, pos=self.pos, with_labels=False, node_size=1,edge_color='black')
        nx.draw_networkx_edges(self.grafo, pos=self.pos, edgelist=arestas_percorridas, edge_color='green', width=4)
        plt.show()

    def busca_em_largura(self, origem, destino):
        visitados = set()
        fila = [(origem, [origem])]  # (vértice, caminho)

        while fila:
            atual, caminho = fila.pop(0)

            if atual == destino:
                self.caminho_em_largura = caminho
                return caminho

            if atual not in visitados:
                visitados.add(atual)

                for vizinho in self.grafo.neighbors(atual):
                    if vizinho not in visitados:
                        fila.append((vizinho, caminho + [vizinho]))

        self.caminho_em_largura = None
        return None
    
    def _calcula_valor_heuristico(self, atual, destino):
        x1, y1 = self.lista_vertices[atual]
        x2, y2 = self.lista_vertices[destino]
        distancia_euclidiana = sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))
        return distancia_euclidiana

    def _fazer_nova_rota(self, caminho_dict, destino):
        caminho = [destino]
        while caminho[-1] is not None:
            caminho.append(caminho_dict[caminho[-1]])
        caminho.reverse()
        return caminho

    def busca_a_estrela(self, origem, destino):
        visitados = set()
        fila = [(origem, 0, 0)]  # (vértice, custo_acumulado, valor_heurístico)
        caminho_dict = {origem: None}

        while fila:
            fila.sort(key=lambda x: x[1] + x[2]) 
            atual, custo_acumulado, _ = fila.pop(0)

            if atual == destino:
                return self._fazer_nova_rota(caminho_dict, destino)

            if atual not in visitados:
                visitados.add(atual)

                for vizinho in self.grafo.neighbors(atual):
                    if vizinho not in visitados:
                        custo = self.grafo.edges[(atual, vizinho)]['weight']
                        custo_acumulado_vizinho = custo_acumulado + custo
                        valor_heuristico = self._calcula_valor_heuristico(vizinho, destino)
                        fila.append((vizinho, custo_acumulado_vizinho, valor_heuristico))
                        caminho_dict[vizinho] = atual
        return None
    
    def _calcular_distancia_percorrida(self, caminho):
        total = 0.0
        for i in range(len(caminho) - 1):
            u, v = caminho[i], caminho[i + 1]
            total += self.grafo[u][v]['weight']
            return total
        
    def _executar_n_algoritimos(self, algoritmo, origem, destino):
        tempo_inicio = time()
        caminho = algoritmo(origem, destino)
        for item in caminho:
            if item is None:
                caminho.remove(item)
        tempo_fim = time()
        tempo_gasto = tempo_fim - tempo_inicio

        if caminho is not None:
            distancia_percorrida = self._calcular_distancia_percorrida(caminho)
            return caminho, distancia_percorrida, tempo_gasto
        else:
            return None, float('inf'), tempo_gasto

    def gerar_estatisticas(self, pares_vertices):
        estatisticas = []
        distancia_media = {}
        tempo_medio = {}

        for origem, destino in pares_vertices:
            # BFS
            _, distancia, tempo = self._executar_n_algoritimos(self.busca_em_largura, origem, destino)
            estatisticas.append(('BFS', origem, destino, distancia, tempo))

            # A*
            _, distancia, tempo = self._executar_n_algoritimos(self.busca_a_estrela, origem, destino)
            estatisticas.append(('A*', origem, destino, distancia, tempo))

        for algoritmo, origem, destino, distancia, tempo in estatisticas:
            if algoritmo not in distancia_media:
                distancia_media[algoritmo] = []
                tempo_medio[algoritmo] = []

            distancia_media[algoritmo].append(distancia)
            tempo_medio[algoritmo].append(tempo)

        for algoritmo in distancia_media:
            media_distancia_algoritmo = self._media(distancia_media[algoritmo])
            media_tempo_algoritmo = self._media(tempo_medio[algoritmo])

            print(f'Algoritmo: {algoritmo}')
            print(f'Distância média percorrida: {media_distancia_algoritmo}')
            print(f'Tempo médio gasto: {media_tempo_algoritmo}')
            print()

#testes
quantidade_elementos = 4000
alcance_medio = 0.015
buscas = Buscas(quantidade_elementos, alcance_medio)
pares_vertices = [(1, 100), (22, 230), (36, 679), (67, 896), (5, 567), (6, 60), (79, 700), (86, 800), (92, 925), (100, 145)]
buscas.gerar_estatisticas(pares_vertices)
