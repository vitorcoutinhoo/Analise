# importa a biblioteca numpy para trabalhar com matrizes
import numpy as np

expanded_matrix = np.matrix([])
with open(r'solve_linear_systems/gauss_elimination/input.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # Constroi a mariz expandida a partir do arquivo de entrada
        # linha a linha de cima para baixo
        row = np.matrix(line.strip().split(' '))
        expanded_matrix = np.vstack([expanded_matrix, row]) if expanded_matrix.size else row

# Resolve a matriz em um array de soluções
def solution(matrix, vector):
    rows, _ = np.shape(matrix)
    x_values = np.zeros((rows, 1))

    # Resolve a matriz da ultima linha em direção a primeira
    # o simbolo @ é o produto matricial
    for i in range(rows - 1, -1,-1):
        x_values[i, 0] = (vector[i, 0] - np.dot(matrix[i, i:rows], x_values[i:rows, 0])) / matrix[i, i]

    return x_values

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


# Resolve o sistema linear Ax = b
def gauss_elimination(matrix, vector):
    rows, _ = np.shape(matrix)
    expanded_A = np.concatenate((matrix, vector), axis=1)
    expanded_A = expanded_A.astype(float)
    expanded_A = change_rows(expanded_A)

    # Forma a matriz triangular superior
    for j in range(rows - 1):
        pivot = expanded_A[j, j]
        for i in range(j + 1, rows):
            factor = expanded_A[i, j] / pivot
            expanded_A[i, 0:] = expanded_A[i, 0:] - factor * expanded_A[j, 0:]
    
    # Separa a matriz expandida em matriz U e vetor y
    U_matrix = expanded_A[0:, 0:rows]
    y_vector = expanded_A[0:, rows:]

    # Resolve o sistema
    x_values = solution(U_matrix, y_vector)
    return x_values

# Ax = b
A = expanded_matrix[0:, 0:-1]
b = expanded_matrix[0:, -1:]
x = gauss_elimination(A, b)

# Escreve o resultado no arquivo de saida
lista = x.flatten().tolist()
with open(r'solve_linear_systems/gauss_elimination/input.txt', 'w', encoding='utf-8') as file:
    for item in lista:
        file.write(f"{item}\n")
