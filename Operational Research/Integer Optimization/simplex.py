import os
import numpy as np

MAX_MODE = 'MAX'
MIN_MODE = 'MIN'
EPSILON = 1e-12  #perturbação

def read_problem_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    c = []
    A = []
    b = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("c ="):
            c = list(map(float, stripped_line[4:].strip().strip('[]').split(',')))
        elif stripped_line.startswith("A ="):
            matrix_data = stripped_line[4:].strip()
            rows = matrix_data.strip().strip('[]').split('], [')
            for row in rows:
                A.append(list(map(float, row.strip().strip('[]').split(','))))
        elif stripped_line.startswith("b ="):
            b = list(map(float, stripped_line[4:].strip().strip('[]').split(', ')))

    c = np.array(c)
    A = np.array(A)
    b = np.array(b)
    
    return c, A, b

"""

 Esta implementação utiliza as seguintes regras para otimizar o processo de seleção de pivôs e lidar com a degenerescência:

 Regra de Dantzig: Utilizada para escolher a variável de entrada na base. A variável com o coeficiente mais negativo na linha da função objetivo é selecionada, maximizando a taxa de melhora por passo (no caso de maximização). Esta é a regra principal para decidir qual coluna entrará na base.

 Perturbação: Introduz um pequeno valor, EPSILON (definido como 1e-8), nas restrições e na função objetivo para ajudar a lidar com problemas de degenerescência, tornando os valores ligeiramente diferentes. Essa perturbação evita que múltiplas variáveis sejam candidatas exatas, reduzindo a chance de ciclos e melhorando a estabilidade numérica.

 Além disso, a implementação inclui uma Fase 1 para lidar com problemas infactíveis, onde uma solução básica inicial é construída antes de entrar na fase principal do método simplex.

"""

class Simplex:
    def __init__(self, mode=MIN_MODE):
        self.main_variables_count = None
        self.restrictions_count = None
        self.basis = None
        self.mode = mode
        self.variables_count = 0
        self.objective_value = 0
        self.iter = 0
        self.status = ""

    def init_table(self, a, b):
        self.table = np.zeros((self.restrictions_count, self.variables_count + 1))
        for i in range(self.restrictions_count):
            for j in range(self.main_variables_count):
                self.table[i][j] = a[i][j]
            for j in range(self.restrictions_count):
                self.table[i][j + self.main_variables_count] = int(i == j)
            self.table[i][-1] = b[i]

    def get_negative_b_row(self):
        row = -1
        for i, a_row in enumerate(self.table):
            if a_row[-1] < 0 and (row == -1 or abs(a_row[-1]) > abs(self.table[row][-1])):
                row = i
        return row

    def remove_negative_b(self):
        while True:
            row = self.get_negative_b_row()
            if row == -1:
                return True

            column = self.get_negative_b_column(row)
            if column == -1:
                return False
            
            self.gauss(row, column)
            self.calculate_f()
            self.print_table()

    def gauss(self, row, column):
        self.table[row] /= self.table[row][column]
        for i in range(self.restrictions_count):
            if i != row:
                self.table[i] -= self.table[row] * self.table[i][column]
        self.basis[row] = column

    def calculate_f(self):
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
        q = []
        for i in range(self.restrictions_count):
            if self.table[i][column] == 0:
                q.append(np.inf)
            else:
                q_i = self.table[i][-1] / self.table[i][column]
                q.append(q_i if q_i >= 0 else np.inf)
        return q

    def get_solve(self):
        y = np.zeros((self.variables_count))
        for i in range(self.restrictions_count):
            y[self.basis[i]] = self.table[i][-1]
        return y
    
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
                self.status = "INFINITO"
                break

            self.table = self.pivot_on(self.table, pivot_row, pivot_col)
        return self.table

    def simplex(self, c: np.array, A: np.array, b: np.array):
        if self.mode == MIN_MODE:
            c = -c

        self.main_variables_count = A.shape[1]
        self.restrictions_count = A.shape[0]
        self.variables_count = self.main_variables_count + self.restrictions_count
        self.basis = [i + self.main_variables_count for i in range(self.restrictions_count)]
        self.c = np.concatenate([c, np.zeros((self.restrictions_count + 1))])
        self.f = np.zeros((self.variables_count + 1))
        self.init_table(A + EPSILON, b + EPSILON)

        if not self.remove_negative_b():
            self.status = 'INFACTÍVEL'
            return
        
        self.table = self.phase_1_simplex()

        self.iter += 1

        while True:
            self.calculate_f()
            self.print_task()
            self.print_table() 

            #regra de dantzig
            candidate_columns = [i for i in range(len(self.f) - 1) if (self.f[i] < 0 if self.mode == MAX_MODE else self.f[i] > 0)]
            if not candidate_columns:
                self.status = 'ÓTIMO'
                break
            
            column = max(candidate_columns, key=lambda i: abs(self.f[i]))

            q = self.get_relations(column)
            if all(qi == np.inf for qi in q):
                self.status = 'INFINITO'
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

    base_output_dir = os.path.join("artifacts", "output")
    os.makedirs(base_output_dir, exist_ok=True)
    folder_path = "problems"
   
    for idx, filename in enumerate(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, filename)
        c, A, b = read_problem_file(file_path)

        simplex = Simplex()
        result = simplex.simplex(c, A, b)

        #import scipy.optimize as opt
        #result = opt.linprog(-c, A, b)
        #print(result)

        print(f"\nProblema {idx+1}\n")
        print(f"Status: {simplex.status}")
        print("Valor Objetivo:", simplex.objective_value)
        print("Iterações:", simplex.iter)
        print("Solução:", simplex.get_solve())