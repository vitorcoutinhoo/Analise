"""
    Universidade Estadual de Santa Cruz - UESC
    Discente: Vítor Coutinho Lima
    Disciplina: Análise numérica

    Este programa realiza a aproximação polinomial contínua
    de um conjunto de dados fornecidos em um arquivo .txt.
"""

import numpy as np
import sympy as sp


def archive_reader(path):
    """
    Esta função recebe o caminho de um arquivo .txt e retorna um dicionário
    com os dados do arquivo.

    O arquivo deve estar no seguinte formato:
    x, valor1, valor2, valor3, ..., valorn
    y, valor1, valor2, valor3, ..., valorn
    """
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
        Esta função recebe o caminho de um arquivo .txt e um dicionário
        e escreve os dados do dicionário no arquivo.

        O arquivo será escrito no seguinte formato:
        a0 = valor
        a1 = valor
        an = valor
    '''

    with open(path, "w", encoding="utf-8") as archive:
        for key in data_dict:
            archive.write(f"{key}: {data_dict[key]}\n")


def pow_x_list(number_of_terms, x_symbol):
    """
    Esta função recebe o número de termos da aproximação polinomial e
    retorna uma lista com os valores de x elevados às potências de 0 até
    number_of_terms - 1.
    """
    powered_x_list = []
    for i in range(number_of_terms):
        powered_x_list.append(x_symbol**i)

    return powered_x_list


def function(strg):
    """
    Esta função recebe uma função em forma de string
    e retorna a função em forma de expressão simbólica.
    """
    return sp.sympify(strg).subs({"x": sp.symbols("x")}).evalf()


def matrix_transormation(x_values, y_value, intv):
    """
    Esta função recebe os valores de x e y e retorna uma matriz
    expandida.
    """

    vector = []
    vector.append(y_value)
    matrix = np.array([])

    for values in x_values:
        row = np.array(values)
        matrix = np.vstack([matrix, row]) if matrix.size else row

    matrix = [
        sp.sympify(matrix[i]).subs({"x": sp.symbols("x")}) for i in range(len(matrix))
    ]
    vector = sp.sympify(vector[0]).subs({"x": sp.symbols("x")})

    row, _ = np.shape(matrix)
    new_matrix = []
    for i in range(row):
        for j in range(row):
            aux = sp.tensorproduct(matrix[i], matrix[j])
            new_matrix.append(aux[0][0])
    new_matrix = np.array(new_matrix).reshape(row, row)

    new_vector = []
    for i in range(row):
        aux = vector * matrix[i]
        new_vector.append(aux)

    new_matrix = np.concatenate((new_matrix, new_vector), axis=1)

    rows, cols = np.shape(new_matrix)
    for i in range(rows):
        for j in range(cols):
            new_matrix[i, j] = sp.integrate(
                new_matrix[i, j], (sp.symbols("x"), intv[0], intv[1])
            )

    return new_matrix


def gauss_elimination(matrix):
    """
    Esta função Utiliza o método de eliminação de gauss para resolver o sistema linear.
    A matriz deve ser expandida.
    """

    rows, _ = np.shape(matrix)
    for j in range(rows - 1):
        pivot = matrix[j, j]
        for i in range(j + 1, rows):
            factor = matrix[i, j] / pivot
            matrix[i, 0:] = matrix[i, 0:] - factor * matrix[j, 0:]

    p_matrix = matrix[0:, 0:rows]
    y_vector = matrix[0:, rows:]

    a_vector = np.zeros((rows, 1))

    for i in range(rows - 1, -1, -1):
        a_vector[i, 0] = (
            y_vector[i, 0] - np.dot(p_matrix[i, i:rows], a_vector[i:rows, 0])
        ) / p_matrix[i, i]

    result_list = []
    for i in range(rows):
        result_list.append(a_vector[i, 0])

    return result_list


def polinomial_aproximation(fnct, intv, number_of_terms):
    """
    Esta função recebe uma função em forma de string e o número de termos
    da aproximação polinomial e retorna uma matriz expandida.
    """
    _x = sp.symbols("x")

    x_list = pow_x_list(number_of_terms, _x)
    matrix = matrix_transormation(x_list, fnct, intv)
    result = gauss_elimination(matrix)

    result_dict = {}
    for i in range(number_of_terms):
        result_dict[f"a{i}"] = result[i]

    return result_dict


data = archive_reader("Relatorio2/polinomial_aproximation2/input.txt")
terms = [int(i) for i in data["qnt"]]
terms = terms[0]

x_intv = [float(i) for i in data["intv"]]

func = [str(i).strip() for i in data["func"]]
func = func[0]

function = function(func)
data = polinomial_aproximation(function, x_intv, terms)
archive_writer("Relatorio2/polinomial_aproximation2/output.txt", data)
