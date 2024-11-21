# Grupo:
# Guilherme Henrique Galdini Tosi - N° USP 11781587
# Amália Vitória de Melo - N° USP 13692417

import os
import numpy as np

# Definição de constantes usadas no algoritmo
MAX_MODE = 'MAX' # Modo de maximização
MIN_MODE = 'MIN' # Modo de minimização
EPSILON = 1e-18 # Perturbação para evitar degeneração e problemas numéricos

# Função para ler arquivos de problemas de programação linear
def read_problem_file(file_path):
    # Lê os dados de um arquivo com formato específico contendo:
    # - c: vetor de custos da função objetivo
    # - A: matriz de coeficientes das restrições
    # - b: vetor de recursos (valores do lado direito das restrições)
    
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    c = [] # Coeficientes da função objetivo
    A = [] # Matriz de coeficientes das restrições
    b = [] # Recursos (vetor b)

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("c ="):
            # Lê o vetor de custos c
            c = list(map(float, stripped_line[4:].strip().strip('[]').split(',')))
        elif stripped_line.startswith("A ="):
            # Lê a matriz A, formatada como listas de listas
            matrix_data = stripped_line[4:].strip()
            rows = matrix_data.strip().strip('[]').split('], [')
            for row in rows:
                A.append(list(map(float, row.strip().strip('[]').split(','))))
        elif stripped_line.startswith("b ="):
            # Lê o vetor b
            b = list(map(float, stripped_line[4:].strip().strip('[]').split(', ')))

    # Converte c, A e b para arrays do numpy
    c = np.array(c)
    A = np.array(A)
    b = np.array(b)
    
    return c, A, b

"""

 Esta implementação utiliza as seguintes regras para otimizar o processo de seleção de pivôs e lidar com a degenerescência:

 Regra de Dantzig: Utilizada para escolher a variável de entrada na base. A variável com o coeficiente mais negativo na linha da função objetivo é selecionada, maximizando a taxa de melhora por passo (no caso de maximização). Esta é a regra principal para decidir qual coluna entrará na base.

 Perturbação: Introduz um pequeno valor, EPSILON (definido como 1e-18), nas restrições e na função objetivo para ajudar a lidar com problemas de degenerescência, tornando os valores ligeiramente diferentes. Essa perturbação evita que múltiplas variáveis sejam candidatas exatas, reduzindo a chance de ciclos e melhorando a estabilidade numérica.

 Além disso, a implementação inclui uma Fase 1 para lidar com problemas infinitos, onde uma solução básica inicial é construída antes de entrar na fase principal do método simplex.

"""
# Classe principal que implementa o Método Simplex.
class Simplex:
    def __init__(self, mode=MIN_MODE):
        """
        Inicializa a classe Simplex.
        mode: Define o modo do problema (minimização ou maximização).
        """
        self.main_variables_count = None   # Número de variáveis de decisão
        self.restrictions_count = None     # Número de restrições    
        self.objective_value = None        # Valor da função objetivo
        self.solution = None               # Solução ótima (se existir)
        self.basis = None                  # Variáveis na base inicial
        self.mode = mode                   # Modo do problema
        self.variables_count = 0           # Número total de variáveis no problema expandido
        self.iter = 0                      # Contador de iterações    
        self.status = ""                   # Status da solução (ÓTIMO, INFACTÍVEL, ILIMITADO)

    def init_table(self, a, b):
        """
        Inicializa a tabela simplex (forma tabular).
        Adiciona variáveis de folga e configura os valores iniciais.
        """
        self.table = np.zeros((self.restrictions_count, self.variables_count + 1))
        for i in range(self.restrictions_count):
            # Adiciona coeficientes das variáveis de decisão
            for j in range(self.main_variables_count):
                self.table[i][j] = a[i][j]
            # Adiciona as variáveis de folga
            for j in range(self.restrictions_count):
                self.table[i][j + self.main_variables_count] = int(i == j)
            # Adiciona o vetor b (coluna dos recursos)
            self.table[i][-1] = b[i]

    def get_negative_b_row(self):
        """
        Identifica a linha com b negativo, necessário para resolver problemas iniciais.
        """
        row = -1
        for i, a_row in enumerate(self.table):
            if a_row[-1] < 0 and (row == -1 or abs(a_row[-1]) > abs(self.table[row][-1])):
                row = i
        return row

    def remove_negative_b(self):
        """
        Resolve inconsistências com b negativo usando o método dual simplex.
        """
        while True:
            row = self.get_negative_b_row()
            if row == -1:
                # Não há mais b negativos, solução factível encontrada
                return True

            # Seleciona a coluna para realizar o pivoteamento
            column = self.get_negative_b_column(row)
            if column == -1:
                # Problema é infactível
                return False
            
            # Realiza o pivoteamento
            self.gauss(row, column)
            self.calculate_f()
            self.print_table()

    def gauss(self, row, column):
        """
        Realiza a operação de pivoteamento na tabela simplex.
        """
        self.table[row] /= self.table[row][column]
        for i in range(self.restrictions_count):
            if i != row:
                self.table[i] -= self.table[row] * self.table[i][column]
        self.basis[row] = column

    def calculate_f(self):
        """
        Recalcula a linha da função objetivo na tabela.
        """
        self.f = -self.c.copy()
        
        for j, basis_var in enumerate(self.basis):
            self.f += self.c[basis_var] * self.table[j]
        
        self.objective_value = self.f[-1]

    def get_negative_b_column(self, row):
        column = -1
        for i, aij in enumerate(self.table[row][:-1]):
            if aij < 0 and (column == -1 or abs(aij) > abs(self.table[row][column])):
                column = i
        return column

    def get_relations(self, column):
        """
        Calcula as razões (relação b/a) para escolher a variável que sai da base.
        """
        q = []
        for i in range(self.restrictions_count):
            if self.table[i][column] == 0:
                q.append(np.inf)
            else:
                q_i = self.table[i][-1] / self.table[i][column]
                q.append(q_i if q_i >= 0 else np.inf)
        return q

    def get_solve(self):
        """
        Retorna a solução atual do problema com base na tabela simplex.
        """
        y = np.zeros((self.variables_count))
        for i in range(self.restrictions_count):
            y[self.basis[i]] = self.table[i][-1]
        self.solution = y
        return self.solution
    
    def phase_1_simplex(self):
        THETA_INFINITE = -1
        opt = False
        n = len(self.table[0])
        m = len(self.table) - 2

        while not opt:
            min_cj = 0.0
            pivot_col = 1
            for j in range(1, n - m):
                cj = self.table[1][j]
                if cj < min_cj:
                    min_cj = cj
                    pivot_col = j
            if min_cj == 0.0:
                opt = True
                continue

            pivot_row = 0
            min_theta = THETA_INFINITE
            for i, xi in enumerate(self.table[2:], start=2):
                xij = xi[pivot_col]
                if xij > 0:
                    theta = xi[0] / xij
                    if theta < min_theta or min_theta == THETA_INFINITE:
                        min_theta = theta
                        pivot_row = i

            if min_theta == THETA_INFINITE:
                self.status = "INFACTÍVEL"
                self.objective_value = None
                self.solution = None
                return 0

            self.table = self.pivot_on(self.table, pivot_row, pivot_col)
        return self.table

    def simplex(self, c: np.array, A: np.array, b: np.array):
        """
        Implementa o algoritmo Simplex, incluindo fase 1 e resolução principal.
        """
        # com os novos casos de teste não é mais necessário, monitor mudou o vetor c para -c
        # if self.mode == MIN_MODE:
        #     c = -c

        self.main_variables_count = A.shape[1]
        self.restrictions_count = A.shape[0]
        self.variables_count = self.main_variables_count + self.restrictions_count
        self.basis = [i + self.main_variables_count for i in range(self.restrictions_count)]
        self.c = np.concatenate([c, np.zeros((self.restrictions_count + 1))])
        self.f = np.zeros((self.variables_count + 1))
        self.init_table(A + EPSILON, b + EPSILON)

        # Fase 1: Resolução inicial para garantir factibilidade
        if not self.remove_negative_b():
            self.status = 'INFACTÍVEL'
            return
        
        self.table = self.phase_1_simplex()
        if self.table.size == 0:
            self.objective_value = None
            return 

        while True:
            
            self.calculate_f()
            self.print_task()
            self.print_table() 
            self.get_solve()

            # Regra de Dantzig para escolher a coluna pivô
            candidate_columns = [i for i in range(len(self.f) - 1) if (self.f[i] < 0 if self.mode == MAX_MODE else self.f[i] > 0)]
            if not candidate_columns:
                self.status = 'ÓTIMO'
                break
            
            column = max(candidate_columns, key=lambda i: abs(self.f[i]))

            q = self.get_relations(column)
            if all(qi == np.inf for qi in q):
                self.status = 'INFINITO'
                self.objective_value = None
                self.solution = None
                break

            row = np.argmin(q)
            self.gauss(row, column)
            self.iter += 1   

    def pivot_on(self, table, pivot_row, pivot_col):
        pivot_value = table[pivot_row][pivot_col]
        table[pivot_row] = [value / pivot_value for value in table[pivot_row]]
        
        for i, row in enumerate(table):
            if i != pivot_row:
                factor = row[pivot_col]
                table[i] = [current - factor * new_value for current, new_value in zip(row, table[pivot_row])]
        return table

    def print_table(self):
        with open(os.path.join('artifacts/output/', 'table.txt'), 'a') as f:
            f.write('     |' + ''.join(['   y%-3d |' % (i + 1) for i in range(self.variables_count)]) + '    b   |\n')
            for i in range(self.restrictions_count):
                f.write('%4s |' % ('y' + str(self.basis[i] + 1)) + ''.join([' %6.2f |' % aij for j, aij in enumerate(self.table[i])]) + '\n')
            if self.status == "ÓTIMO":
                f.write('   F |' + ''.join([' %6.2f |' % aij for aij in self.f]) + '\n')
                f.write('   y |' + ''.join([' %6.2f |' % xi for xi in self.get_solve()]) + '\n\n')

    def print_coef(self, ai, i):
        if ai == 1:
            return 'y%d' % (i + 1)
        if ai == -1:
            return '-y%d' % (i + 1)
        return '%.2fy%d' % (ai, i + 1)

    def print_task(self):
        with open(os.path.join('artifacts/output/', 'task.txt'), 'a') as f:
            f.write(' + '.join(['%.2fy%d' % (ci, i + 1) for i, ci in enumerate(self.c[:self.main_variables_count]) if ci != 0]) + ' -> min\n')
            for i, a_row in enumerate(self.table):
                f.write(' + '.join([self.print_coef(ai, j) for j, ai in enumerate(a_row[:self.main_variables_count]) if ai != 0]) + ' = %.2f\n' % a_row[-1])

if __name__ == "__main__":
    # Executa o método simplex para cada problema na pasta "problems"
    
    base_output_dir = os.path.join("artifacts", "output")
    os.makedirs(base_output_dir, exist_ok=True)
    folder_path = "problems"

    for idx, filename in enumerate(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, filename)
        c, A, b = read_problem_file(file_path)

        model = Simplex()
        
        model.simplex(c, A, b)

        print(f"\nProblema {idx+1}\n")
        print(f"Status: {model.status}")
        print("Iterações:", model.iter)
        print("Valor Ótimo:", model.objective_value)
        print("Solução:", model.solution)
        
