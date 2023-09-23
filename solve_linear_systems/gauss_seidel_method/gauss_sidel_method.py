# Importando a biblioteca numpy
import numpy as np

expanded_matrix = np.matrix([])
error = np.array([])
with open(r"solve_linear_systems\gauss_seidel_method\input.txt", "r", encoding='utf-8') as file:
    # Recupera a precisão
    error = file.readline().strip().split(" ")

    for line in file:
        # Constroi a mariz expandida a partir do arquivo de entrada
        # linha a linha de cima para baixo
        row = np.matrix(line.strip().split(" "))
        expanded_matrix = np.vstack([expanded_matrix, row]) if expanded_matrix.size else row

error = np.array(error).astype(float)

# verifica se a matriz converge
def verify_matrix(matrix):
    rows,_ = np.shape(matrix)
    aux = 0
    for i in range(rows):
        for j in range(rows):
            if i != j:
                aux += abs(matrix[i, j])
                if abs(matrix[i, i]) >= aux:
                    return True
                else:
                    return False

# Resolve o sistema linear Ax = b
def gauss_seidel_method(matrix, error_tolerance):
    matrix = matrix.astype(float)  
    rows, _ = np.shape(matrix)  

    # Verifica se a matriz converge
    if not verify_matrix(matrix): 
        return None

    # Separa a matriz A e o vetor b
    # cria o vetor x
    A_matrix = matrix[:, :-1]  
    b_vector = matrix[:, -1]  
    x_vector = np.zeros(rows)  

    # loop principal
    while True:
        # Faz uma cópia do vetor x atual para verificar a convergência
        old_x = x_vector.copy()

        for i in range(rows):
            # Atualiza cada elemento do vetor x usando o método de Gauss-Seidel
            x_vector[i] = (b_vector[i] - np.dot(A_matrix[i, :i], x_vector[:i]) - np.dot(A_matrix[i, i+1:], x_vector[i+1:])) / A_matrix[i, i]
        
        # Calcula o erro como a norma da diferença entre x atual e o anterior
        x_error = np.linalg.norm(x_vector - old_x)  

        # Sai do loop se o erro estiver abaixo da tolerância
        if x_error <= error_tolerance:
            break  

    return x_vector 

# Imprime o resultado
result = gauss_seidel_method(expanded_matrix, error)
lista = result.flatten().tolist()
with open(r"solve_linear_systems\gauss_seidel_method\output.txt", "w", encoding='utf-8') as file:
    for i in lista:
        file.write(str(i) + "\n")

