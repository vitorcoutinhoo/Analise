'''
    Universidade Estadual de Santa Cruz - UESC
    Discente: Vítor Coutinho Lima
    Disciplina: Análise numérica

    Este programa realiza a aproximação polinomial discreta
    de um conjunto de dados fornecidos em um arquivo .txt.
'''

#from math import sqrt
#import matplotlib.pyplot as plt
import numpy as np

def archive_reader(path):
    '''
        Esta função recebe o caminho de um arquivo .txt e retorna um dicionário
        com os dados do arquivo.

        O arquivo deve estar no seguinte formato:
        x, valor1, valor2, valor3, ..., valorn
        y, valor1, valor2, valor3, ..., valorn
    '''
    data_dict = {}
    values = ()
    with open(path, "r", encoding="utf-8") as archive:
        for line in archive:
            values = line.strip().split(",")
            index = values[0]

            data_dict[index] = values[1:]

    return data_dict

def archive_writer(path, data_dict):
    '''
        Esta função recebe o caminho de um arquivo .txt e um dicionário com os
        dados a serem escritos no arquivo.

        O arquivo será escrito no seguinte formato:
        a0 = valor
        a1 = valor
        an = valor
    '''
    with open(path, "w", encoding="utf-8") as archive:
        for key in data_dict:
            archive.write(f"{key}: {data_dict[key]}\n")

def pow_x_values(x_values, number_of_terms):
    '''
        Esta função recebe uma lista de valores de x e o número de termos da
        aproximação polinomial e retorna uma lista com os valores de x
        elevados às potências de 0 até number_of_terms - 1.
    '''
    powered_x_values = {}
    for i in range(number_of_terms):
        key = f"u{i}"
        powered_x_values[key] = [x**i for x in x_values]

    return powered_x_values

def matrix_transormation(x_values, y_values):
    '''
        Esta função recebe os valores de x e y e retorna uma matriz
        expandida.
    '''
    vector = np.array([])
    matrix = np.array([])

    for _, values in x_values.items():
        row = np.array(values)
        matrix = np.vstack([matrix, row]) if matrix.size else row
        
        aux = np.dot(y_values, values)
        vector = np.vstack((vector, aux)) if vector.size else aux
        
    row, _ = np.shape(matrix)
    new_matrix = np.zeros((row, row))
    for i in range(row):
        for j in range(row):
            new_matrix[i, j] = matrix[i] @ matrix[j]
            
    new_matrix = np.concatenate((new_matrix, vector), axis=1)
    return new_matrix

def gauss_elimination(matrix):
    '''
        Esta função recebe uma matriz uma lista com os
        valores das incógnitas.

        Utiliza o método de eliminação de gauss para resolver o sistema linear.
        A matriz deve ser expandida.
    '''
    
    rows, _ = np.shape(matrix)

    # Forma a matriz triangular superior
    for j in range(rows - 1):
        pivot = matrix[j, j]
        for i in range(j + 1, rows):
            factor = matrix[i, j] / pivot
            matrix[i, 0:] = matrix[i, 0:] - factor * matrix[j, 0:]
            
    # Separa a matriz expandida em matriz U e vetor y
    p_matrix = matrix[0:, 0:rows]
    y_vector = matrix[0:, rows:]

    a_vector = np.zeros((rows, 1))
    # Resolve a matriz da ultima linha em direção a primeira
    for i in range(rows - 1, -1,-1):
        a_vector[i, 0] = (y_vector[i, 0] - np.dot(p_matrix[i, i:rows], a_vector[i:rows, 0])) / p_matrix[i, i]

    result_list = []
    for i in range(rows):
        result_list.append(a_vector[i, 0])

    return result_list


def polinomial_aproximation(x_values, y_values, number_of_terms):
    '''
        Esta função recebe uma lista de valores de x, uma lista de valores de y
        e o número de termos da aproximação polinomial e retorna uma lista com
        os coeficientes da aproximação polinomial.
    '''
    list_x = pow_x_values(x_values, number_of_terms)
    list_y = y_values

    matrix = matrix_transormation(list_x, list_y)
    result = gauss_elimination(matrix)

    result_data = {}
    for i in range(number_of_terms):
        key = f"a{i}"
        result_data[key] = result[i]

    return result_data


data = archive_reader("Relatorio2/polinomial_aproximation1/input.txt")
terms = [int(x) for x in data["qnt"]]
terms = terms[0]

X = [float(x) for x in data["x"]]
Y = [float(y) for y in data["y"]]

data = polinomial_aproximation(X, Y, terms)
archive_writer("Relatorio2/polinomial_aproximation1/output.txt", data)
