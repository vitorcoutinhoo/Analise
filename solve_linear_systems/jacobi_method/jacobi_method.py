# importando a biblioteca numpy
import numpy as np

expanded_matrix = np.matrix([])
error = np.array([])
with open(r"solve_linear_systems\jacobi_method\input.txt", "r", encoding='utf-8') as file:
    # Recupera a precisão
    error = file.readline().strip().split(" ")

    for line in file:
        # Constroi a mariz expandida a partir do arquivo de entrada
        # linha a linha de cima para baixo
        row = np.matrix(line.strip().split(" "))
        expanded_matrix = np.vstack([expanded_matrix, row]) if expanded_matrix.size else row

error = np.array(error).astype(float)

def verify_matrix(matrix):
    rows,_ = np.shape(matrix)
    sum = 0
    for i in range(rows):
        for j in range(rows):
            if i != j:
                sum += abs(matrix[i, j])
                if abs(matrix[i, i]) >= sum:
                    return True
                else:
                    return False
        
# Resolve o sistema linear Ax = b
def jacobi_method(matrix, error_tolerance):
    matrix = matrix.astype(float)
    rows, _ = np.shape(matrix)
    if not verify_matrix(matrix):
        return None

    # Separa a matriz A e o vetor b
    # cria o vetor x
    A_matrix = matrix[0:, 0:-1]
    b_vector = matrix[0:, -1:]
    x_vector = np.zeros(rows)

    # Cria a matriz -B e o vetor d
    B_matrix = np.zeros((rows, rows))
    d_vector = np.zeros((rows))

    for i in range(rows):
        B_matrix[i,:] = A_matrix[i,:] / A_matrix[i, i]
        d_vector[i] = b_vector[i] / A_matrix[i, i]
        B_matrix[i, i] = 0
    B_matrix = -B_matrix

    # Calcula o vetor x
    old_x = x_vector.copy()
    x_vector = np.dot(B_matrix, x_vector) + d_vector
    x_error = np.linalg.norm(x_vector - old_x)

    # Enquanto o erro for maior que a tolerância
    while x_error.all() > error_tolerance:
        old_x = x_vector.copy()
        x_vector = np.dot(B_matrix, x_vector) + d_vector
        x_error = np.linalg.norm(x_vector - old_x)

    return x_vector

# Escrita da solução no arquivo de saída
x = jacobi_method(expanded_matrix, error)
lista = x.flatten().tolist()
with open(r"solve_linear_systems\jacobi_method\output.txt", "w", encoding='utf-8') as file:
    for item in lista:
        file.write(str(item) + "\n")

