# • Acurácia é calculada pela fórmula: (VP + VN) / (VP + FP + FN + VN)
# • Precisão é calculada pela fórmula: VP / (VP + FP)

# • VP (Verdadeiro Positivo): Casos em que o modelo previu corretamente a classe positiva.
# • FP (Falso Positivo ou Erro Tipo I): Casos em que o modelo previu incorretamente a classe positiva.
# • FN (Falso Negativo ou Erro Tipo II): Casos em que o modelo previu incorretamente a classe negativa.
# • VN (Verdadeiro Negativo): Casos em que o modelo previu corretamente a classe negativa.

# Função para calcular as métricas (acurácia e precisão) de uma matriz
def calculate_metrics(tp, fp, fn, tn):
    accuracy = (tp + tn) / (tp + fp + fn + tn)
    precision = tp / (tp + fp)
    return accuracy, precision

# Função para determinar a matriz com o melhor desempenho com base nas métricas calculadas
def best_performance(matrices):
    best_index = 0
    best_accuracy = 0
    best_precision = 0

    for index, matrix in enumerate(matrices):
        # Extrai os valores da matriz e converte para int
        tp, fp, fn, tn = map(int, matrix)

        # Calcula a acurácia e precisão da matriz atual
        accuracy, precision = calculate_metrics(tp, fp, fn, tn)

        # Verifica se a métrica combinada é melhor do que a atual melhor métrica
        if accuracy + precision > best_accuracy + best_precision:
            best_index = index + 1  # O índice começa em 1, não em 0 por ser um enum
            best_accuracy = accuracy
            best_precision = precision

    return best_index, round(best_accuracy, 2), round(best_precision, 2)

# Entrada do usuário
n = int(input())
matrices = []

# Obtém as matrizes do usuário
for _ in range(n):
    matrix_str = input()
    matrices.append(matrix_str.split(','))

# Calcula o índice, acurácia e precisão da matriz com o melhor desempenho
best_index, best_accuracy, best_precision = best_performance(matrices)

# Exibe os resultados
print(f"Índice: {best_index}")
print(f"Acurácia: {best_accuracy}")
print(f"Precisão: {best_precision}")
