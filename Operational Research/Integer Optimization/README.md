# SME0510 - Introdução à Pesquisa Operacional

## Integrantes:
- **Guilherme Henrique Galdini Tosi** - N° USP 11781587
- **Amália Vitória de Melo** - N° USP 13692417
- **Vinicius Santos Monteiro** - N° USP 11932463

## Descrição do Algoritmo

O código desenvolvido é uma solução para um problema de otimização de um plano diretor de cidade, onde o objetivo é alocar recursos (casas, parques e fábricas) de maneira a maximizar um valor objetivo, levando em conta restrições de conectividade e custos. O problema é modelado utilizando a programação linear inteira e resolvido com a biblioteca `pulp`.

O problema escolhido foi o problem_1.txt, disponibilizado no arquivo problems.zip, mas para teste foram executados todos os arquivos disponibilizados no problems.zip, e também os do problems_2.zip. Basicamente, o programa itera sobre as duas pastas e armazena os resultados do modelo e imagem do grafo resultante. o resultado da execução da instância escolhida por nós fica originalmente armaznada em `results/` ou ` test_results/` (a depender do parâmetro testing), mas com o nome `single_problem_1.png` e `single_problem_1.txt`

A função objetivo do programa original é `Z = (2 * N^2 + 1) * L + F`, o que bastava para otimizar LUCRO e FELICIDADE, apenas. No caso, aqui tivemos uma  otimização também de HABITANTES e CUSTO, na ordem decrescente de prioridade L -> F -> C -> H, resultando em `Z = (2 * N ** 2 + 1) * L + 1e-1 * F - 1e-7 * C + H * 1e-12`, onde as perturbações(pesos) atreladas a cada restrição do modelo garantiram que se houvesse o máximo resultado possível das soluções.

### Funções do Código

#### `create_binary_vars(N: int)`
Essa função cria variáveis binárias para representar a alocação dos três tipos de recursos (Casa, Parque, Fábrica) em cada vértice, além de variáveis auxiliares de conectividade entre os vértices.

**Parâmetros:**
- `N`: Número de vértices no grafo.

**Retorno:**
- Variáveis binárias para cada tipo de recurso (`x_C`, `x_P`, `x_F`).
- Variáveis de conectividade entre os tipos de recursos (`z_CP`, `z_CF`, `z_PF`).

#### `read_matrix_from_file(filename: str)`
Essa função lê uma matriz de um arquivo de texto. Cada linha é interpretada como um vetor de números flutuantes.

**Parâmetros:**
- `filename`: Nome do arquivo a ser lido.

**Retorno:**
- Uma matriz `array` contendo os dados lidos.

#### `create_graph(A: array, positions: array, solution: list, happiness: int)`
Cria um grafo a partir das matrizes de conectividade e das posições dos vértices, e atribui cores aos nós e arestas de acordo com a solução do problema.

**Parâmetros:**
- `A`: Matriz de conectividade entre os vértices.
- `positions`: Posições dos vértices no plano.
- `solution`: Solução obtida para a alocação de recursos.
- `happiness`: Valor inicial da felicidade.

**Retorno:**
- O grafo criado.
- Valores de lucro e felicidade.
- As cores dos nós e arestas.

#### `save_graph(A, graph: Graph, position: array, node_colors: list, edge_colors: list, total_cost: int, inhabitants: int, happiness: int, profit: int, output_plot_filename)`
Plota o grafo usando `matplotlib` e salva a figura gerada. As informações de custo total, felicidade e lucro são adicionadas ao gráfico como legenda.

**Parâmetros:**
- `A`: matriz de adjacências.
- `graph`: Grafo gerado.
- `position`: Posições dos nós.
- `node_colors`: Cores dos nós.
- `edge_colors`: Cores das arestas.
- `total_cost`: Custo total da solução.
- `inhabitants`: Número de habitantes (casas).
- `happiness`: Nível de felicidade.
- `profit`: Lucro.
- `output_plot_filename`: Nome do arquivo de saída.

**Retorno:**
- Salva a figura gerada no arquivo especificado.

#### `plot_graph(output_plot_filename: str)`
Plota o grafo gerado pela função save_graph, a partir do caminho absluto ou relativo

**Parâmetros:**
- `output_plot_filename`: caminho do arquivo gerado pela função sabe_graph.

**Retorno:**
- Plota a imagem do grafo a partir do arquivo do grafo gerado.

#### `tabu_search(A, N, initial_solution, iterations=100000, tenure=10, diversity_factor=3, max_no_improve=100)`
Executa a busca tabu para encontrar a solução otimizada, levando em conta a penalidade de diversidade.

**Parâmetros:**
- `A`: Matriz de conectividade.
- `N`: Número de vértices.
- `initial_solution`: Solução inicial.
- `iterations`: Número de iterações da busca.
- `tenure`: Tempo de permanência de uma solução na lista tabu.
- `diversity_factor`: Fator de penalização da diversidade.
- `max_no_improve`: Número máximo de iterações sem melhoria.

**Retorno:**
- Melhor solução encontrada.
- Custo da melhor solução.

#### `calculate_cost(A, solution)`
Calcula o custo total da solução, incluindo felicidade e lucro, com base na alocação de recursos.

**Parâmetros:**
- `A`: Matriz de conectividade.
- `solution`: Solução de alocação de recursos.


#### `optimize_and_save_graph(problem_file, output_graph_filename, output_txt_file, testing=False)`
Executa a busca tabu para encontrar a solução otimizada, levando em conta a penalidade de diversidade.

**Parâmetros:**
- `problem_file`: arquivo contendo a matriz de adjacências e as posições dos vértices
- `output_graph_filename`: nome do arquivo PNG do grafo resultante
- `output_txt_file`: nome do arquivo txt contendo a solução
- `testing`: boolean para usar os casos de teste ou casos reais

**Retorno:**
- Melhor solução encontrada.
- Grafo gerado
- Solução escrita em arquivo

#### `test_single_file(file_path, output_graph_filename, output_txt_filename, testing)`
Executa a função de otimização para um dado arquivo

**Parâmetros:**
- `file_path`: caminho do arquivo
- `output_graph_filename`: nome do arquivo PNG do grafo resultante
- `output_txt_file`: nome do arquivo txt contendo a solução
- `testing`: boolean para usar os casos de teste ou casos reais

**Retorno:**
- Melhor solução encontrada.
- Grafo gerado
- Solução escrita em arquivo

## Estrutura do Código

1. **Definições iniciais**: 
   - O custo de cada tipo de vértice é definido no dicionário `VERTEX_COSTS`.
   - Funções de criação de variáveis e leitura de arquivos são chamadas.

2. **Modelagem do Problema**:
   - O problema é modelado como uma programação linear inteira, onde a função objetivo é maximizar o valor de `L` (conectividade dos tipos de recursos), `F` (restrições de conectividade),
     `C`(restrições de custos) e `H`(restrições de população)
   - Restrições de conectividade entre os vértices são adicionadas ao modelo.

3. **Solução**:
   - A solução do problema é obtida utilizando o método `model.solve()` da biblioteca `pulp`.
   - A solução é então mapeada para uma alocação de recursos nos vértices, com o cálculo do custo total, felicidade e lucro.

4. **Visualização**:
   - O grafo é gerado e salvo em disco, destacando as alocações e a conectividade entre os recursos.
   - A solução e as estatísticas finais (custo total, número de habitantes, felicidade e lucro) são salvas em um arquivo de texto, assim como aparecem na legenda do grafo.

## Como Rodar o Código

1. **Instalar Dependências**:
   O código utiliza as bibliotecas Python `networkx`, `numpy`, `pulp` e `matplotlib`. Você pode instalar as dependências com o comando:

   ```bash
   pip install networkx numpy pulp matplotlib

2. **Arquivos de entrada**:
  - O código espera dois arquivos de entrada no formato de matriz:

    - problem.txt: Matriz de conectividade entre os vértices.
    - positions.txt: Posições dos vértices.

- Exemplo de estrutura de um arquivo de entrada:

```bash

problem_{n}.txt

0 1 0
1 0 1
0 1 0

0 0
1 1
2 2
```

## 3. Execução do script:

 ```bash
Linux:
python3 script.py

Windows:
python script.py

```

## 4. Exemplo de Saída: 

- A saída do código inclui o seguinte conteúdo no arquivo solution.txt:

```bash

Solucao Otima:
Vertice 1: Casa
Vertice 2: Parque
Vertice 3: Fábrica

Custo Total: 57600
Numero de Habitantes: 1
Nivel de Felicidade: 1
Lucro Total: 1
Tempo: 123456 segundos

```

- Além disso, um gráfico e um txt referentes ao iésimo-problema será salvo em results/graph.png.

## Conclusão: 

```bash 
Este projeto aplica técnicas de otimização e programação linear inteira para resolver um problema de alocação de recursos urbanos, considerando fatores como custo, felicidade e lucro. A solução é visualizada por meio de um grafo, facilitando a análise e interpretação dos resultados.
```