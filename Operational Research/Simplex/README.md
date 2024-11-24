# Método Simplex

Este repositório implementa o algoritmo Simplex para resolver problemas de programação linear. O algoritmo processa os dados de arquivos `.txt` estruturados e retorna os resultados otimizados.

---

## Como Utilizar

### 1. Estrutura do Diretório
- Crie uma pasta chamada `problems` no diretório raiz do projeto.
- Adicione arquivos `.txt` contendo os problemas no seguinte formato:
  - **C**: Vetor com os coeficientes da função objetivo.
  - **A**: Matriz das restrições.
  - **b**: Vetor dos limites das restrições.

O algoritmo processará automaticamente os dados, realizando o parse para estruturas `numpy.array`.

---

### 2. Formato do Arquivo de Entrada
Cada arquivo deve seguir o seguinte formato:

```plaintext
c = [valores de C separados por vírgula]
A = [[valores da matriz A separados por vírgula em cada linha]]
b = [valores de b separados por vírgula]
```

#### 2.1 EXEMPLO

```

c = [1, 4, 6, 9, 4, 3, 4, 5, 1, 3, 1, 6, 5, 9, 1, 8, 7, 6, 5, 7, 7, 7, 1, 2, 4, 2, 3, 3, 2, 2]
A = [[7, 4, 8, 3, 9, 5, 8, 3, 1, 1, 7, 1, 4, 6, 7, 9, 4, 8, 6, 6, 8, 3, 7, 8, 6, 5, 4, 5, 6, 2],
     [5, 3, 1, 4, 5, 4, 7, 4, 2, 2, 6, 2, 9, 1, 5, 2, 8, 8, 4, 8, 2, 5, 3, 9, 1, 2, 5, 2, 1, 9],
     [4, 5, 1, 4, 1, 7, 2, 2, 2, 7, 8, 1, 4, 4, 2, 9, 2, 2, 8, 7, 5, 8, 8, 1, 8, 4, 3, 7, 5, 6],
     [2, 8, 6, 2, 6, 9, 2, 3, 6, 8, 6, 9, 3, 2, 3, 3, 1, 5, 5, 8, 4, 9, 8, 6, 4, 1, 7, 7, 8, 7],
     [2, 4, 6, 9, 4, 4, 7, 6, 7, 7, 4, 5, 5, 4, 3, 9, 9, 9, 6, 3, 8, 3, 3, 6, 5, 7, 2, 3, 9, 5],
     [6, 7, 5, 1, 5, 8, 8, 6, 1, 9, 7, 8, 2, 4, 4, 5, 3, 5, 2, 2, 5, 3, 4, 7, 8, 7, 3, 7, 7, 5],
     [9, 8, 2, 3, 5, 2, 3, 2, 9, 2, 3, 9, 2, 4, 8, 5, 5, 1, 3, 5, 4, 6, 1, 8, 8, 3, 3, 3, 2, 1],
     [8, 2, 8, 2, 8, 9, 7, 6, 1, 4, 9, 4, 3, 1, 8, 2, 4, 7, 9, 5, 8, 5, 5, 6, 7, 6, 4, 6, 7, 3],
     [3, 1, 9, 5, 4, 4, 5, 2, 3, 7, 1, 4, 1, 7, 6, 6, 7, 3, 2, 5, 9, 8, 5, 4, 2, 1, 1, 3, 5, 2],
     [4, 9, 8, 3, 8, 9, 7, 6, 1, 8, 9, 5, 6, 2, 1, 5, 5, 2, 8, 6, 9, 1, 2, 8, 6, 6, 7, 1, 7, 2]]
b = [43, 41, 28, 37, 17, 33, 35, 22, 24, 49]
```

### 3 COMO UTILIZAR

```
Windows

- Execute o seguinte comando no terminal:

- python simplex.py

```

```
Linux

- Execute o seguinte comando no terminal:

- python3 simplex.py

```

### 4 SAÍDAS

Ao executar o algoritmo com os arquivos na pasta problems/, os seguintes resultados serão gerados:

```plaintext

Diretório artifacts/output/
Contém:
table.txt: Arquivo detalhando os cálculos realizados pelo método Simplex.
task.txt: Resumo das movimentações realizadas pelo algoritmo.

```

#### 3.1 OBSERVAÇÕES

```plaintext

- Utilize versões recentes do Python e do NumPy para evitar problemas de compatibilidade.
- Certifique-se de que os arquivos .txt estejam no formato correto para garantir o funcionamento do parse.
- Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

```