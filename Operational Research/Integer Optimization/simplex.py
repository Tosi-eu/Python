import os
import numpy as np

MAX_MODE = 'MAX'
MIN_MODE = 'MIN'
EPSILON = 1e-8  

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
            b = list(map(float, stripped_line[4:].strip().strip('[]').split(',')))

    c = np.array(c)
    A = np.array(A)
    b = np.array(b)
    
    return c, A, b

class SimplexMethod:
    def __init__(self, c, a, b, mode=MIN_MODE):
        self.main_variables_count = a.shape[1]
        self.restrictions_count = a.shape[0]
        self.variables_count = self.main_variables_count + self.restrictions_count
        self.mode = mode
        self.c = np.concatenate([c, np.zeros((self.restrictions_count + 1))])
        self.f = np.zeros((self.variables_count + 1))
        self.basis = [i + self.main_variables_count for i in range(self.restrictions_count)]
        self.init_table(a + EPSILON, b + EPSILON) #perturbação
        self.iter = 0
        self.objective_value = 0
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
        self.objective_value = 0 
        for i in range(self.variables_count + 1):
            self.f[i] = -self.c[i]
            for j in range(self.restrictions_count):
                self.f[i] += self.c[self.basis[j]] * self.table[j][i]
        
        self.objective_value = sum(self.f)

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

    def solve(self):
        self.calculate_f()

        if not self.remove_negative_b():
            self.status = 'INFACTÍVEL'
            return 'INFACTÍVEL'

        self.iter += 1

        while True:
            self.calculate_f()
            self.print_task()

            print('\nIteração', self.iter)
            self.print_table() 

            if all(fi >= 0 if self.mode == MAX_MODE else fi <= 0 for fi in self.f[:-1]):
                self.status = 'ÓTIMO'
                return 'ÓTIMO'

            #Regra de Bland
            candidate_columns = [i for i in range(len(self.f) - 1) if (self.f[i] < 0 if self.mode == MAX_MODE else self.f[i] > 0)]
            if not candidate_columns:
                self.status = 'ÓTIMO'
                return 'ÓTIMO'
            column = min(candidate_columns)

            q = self.get_relations(column)
            if all(qi == np.inf for qi in q):
                self.status = 'INFINITO'
                return 'INFINITO'

            row = np.argmin(q)
            self.gauss(row, column)
            self.iter += 1   

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

    def print_task(self, full=False):
        with open(os.path.join('artifacts/output/', 'task.txt'), 'a') as f:
            f.write(' + '.join(['%.2fy%d' % (ci, i + 1) for i, ci in enumerate(self.c[:self.main_variables_count]) if ci != 0]) + ' => ' + self.mode + '\n')
            for row in self.table:
                if full:
                    f.write(' + '.join([self.print_coef(ai, i) for i, ai in enumerate(row[:self.variables_count]) if ai != 0]) + ' = ' + str(row[-1]) + '\n')
                else:
                    f.write(' + '.join([self.print_coef(ai, i) for i, ai in enumerate(row[:self.main_variables_count]) if ai != 0]) + ' <= ' + str(row[-1]) + '\n')
            f.write('\n')

    def make_dual(a, b, c):
        return -a.T, -c, b

if __name__ == "__main__":

    # necessário que a pasta artifacts pré exista
    base_output_dir = os.path.join("artifacts", "output")

    os.makedirs(base_output_dir, exist_ok=True)
    folder_path = "problems"
   
    for idx, filename in enumerate(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, filename)
        c, A, b = read_problem_file(file_path)

        simplex = SimplexMethod(-c, A, b)
        result = simplex.solve()

        # import scipy.optimize as opt
        # result = opt.linprog(c, A, b)
        # print(result)

        print(f"\nProblema {idx+1}\n")
        print(f"Status: {simplex.status}")
        print("Valor Objetivo:", simplex.objective_value)
        print("Iterações:", simplex.iter)
        print("Solução:", simplex.get_solve())