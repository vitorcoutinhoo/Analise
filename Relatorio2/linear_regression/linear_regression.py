'''
    Universidade Estadual de Santa Cruz - UESC
    Discente: Vítor Coutinho Lima
    Disciplina: Análise numérica

    Este programa realiza a regressão linear de um conjunto de dados
    fornecidos em um arquivo .txt.
'''

from math import sqrt
#import matplotlib.pyplot as plt

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
        r = valor
    '''
    with open(path, "w", encoding="utf-8") as archive:
        for key in data_dict:
            archive.write(f"{key}: {data_dict[key]}\n")

def square_sum(list_values):
    '''
        Esta função recebe uma lista de valores e retorna a soma dos quadrados
        dos valores da lista.

    '''
    total = 0
    for item in list_values:
        total += item**2

    return total


def mult(x_list, y_list):
    '''
        Esta função recebe duas listas de valores e retorna a soma dos produtos
        dos valores das listas.
    '''
    total = 0
    for _x, _y in zip(x_list, y_list):
        total += _x * _y

    return total

def change_type(item_list):
    '''
        Esta função recebe uma lista de valores e retorna uma lista com os
        valores convertidos para float.
    '''
    item_list = [float(item) for item in item_list]

    return item_list

def linear(x_values, y_values):
    '''
        Esta função recebe duas listas de valores e retorna os coeficientes
        A0, A1 e o coeficiente de correlação.
    '''
    _n = len(x_values)
    x_total = sum(x_values)
    y_total = sum(y_values)

    aux1 = (_n * mult(x_values, y_values)) - (x_total * y_total)
    aux2 = (_n * square_sum(x_values)) - (x_total**2)
    a1_value = aux1 / aux2

    a0_value = (y_total / _n) - a1_value * (x_total / _n)

    aux3 =  sqrt(aux2) * sqrt((_n * square_sum(y_values) - y_total**2))
    r_value = aux1 / aux3

    return {"a0": a0_value, "a1": a1_value, "r": r_value}


data = archive_reader("input.txt")

X = change_type(data["x"])
Y = change_type(data["y"])

data = linear(X, Y)
archive_writer("output.txt", data)

# plt.scatter(X, Y)
# plt.plot(X, [a0 + a1 * x for x in X], color="red")
# plt.show()
