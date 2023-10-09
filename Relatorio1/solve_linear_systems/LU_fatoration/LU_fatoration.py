# importa a biblioteca numpy para trabalhar com matrizes
import numpy as np
import time

expanded_matrix = np.matrix([])
with open(r"solve_linear_systems\LU_fatoration\input.txt", "r", encoding="utf-8") as file:
    for line in file:
        # Constroi a mariz expandida a partir do arquivo de entrada
        # linha a linha de cima para baixo
        row = np.matrix(line.strip().split(" "))
        expanded_matrix = np.vstack([expanded_matrix, row]) if expanded_matrix.size else row

# Troca as linhas da matriz para que o pivô não seja zero
def change_rows(matrix):
    rows, _ = np.shape(matrix)
    # Procura uma linha que tenha o pivô igual de zero
    for i in range(rows):
        if matrix[i, i] == 0:
            # Troca a linha por uma linha abaixo da linha atual que tenha o pivô diferente de zero
            for j in range(i + 1, rows):
                if matrix[j, i] != 0:
                    matrix[[i, j]] = matrix[[j, i]]
                    break
    return matrix

# Fatora a matriz em L e U
def LU_fatoration(matrix):
    # Converte a matriz para float
    matrix = matrix.astype(float)
    matrix = change_rows(matrix)

    # Inicializa as matrizes L e U
    rows, _ = np.shape(matrix)
    L_matrix = np.identity(rows)
    U_matrix = np.zeros((rows, rows))

    # Fatora a matriz em L e U
    for i in range(rows):
        for j in range(i, rows):
            # Calcula o valor de U
            U_matrix[i, j] = matrix[i, j] - sum(L_matrix[i, k] * U_matrix[k, j] for k in range(i))
        for j in range(i + 1, rows):
            # Calcula o valor de L
            L_matrix[j, i] = (matrix[j, i] - sum(L_matrix[j, k] * U_matrix[k, i] for k in range(i))) / U_matrix[i, i]

    return solution(L_matrix, U_matrix, matrix[0:, -1:])

def solution(L, U, b):
    rows, _ = np.shape(L)
    y_vector = np.zeros((rows, 1))
    x_values = np.zeros((rows, 1))

    # Resolve o sistema linear Ly = b
    for i in range(rows):
        y_vector[i, 0] = (b[i, 0] - sum(L[i, k] * y_vector[k, 0] for k in range(i))) / L[i, i]

    # Resolve o sistema linear Ux = y
    for i in range(rows - 1, -1, -1):
        x_values[i, 0] = (y_vector[i, 0] - sum(U[i, k] * x_values[k, 0] for k in range(i + 1, rows))) / U[i, i]

    return x_values

start = time.perf_counter()
result = LU_fatoration(expanded_matrix)
end = time.perf_counter()


lista = result.flatten().tolist()
with open(r"solve_linear_systems\LU_fatoration\output.txt", "w", encoding="utf-8") as file:
    for i in range(len(lista)):
        file.write(f"i{i + 1}: {lista[i]}\n")
    file.write(f"\nTempo de execução: {end - start} segundos")