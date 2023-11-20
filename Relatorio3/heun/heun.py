"""
Universidade Estadual de Santa Cruz - UESC
Discente: Vítor Coutinho Lima

Método de Heun para resolução de EDOs de primeira ordem.
"""

import sympy as sp
import pandas as pd


def read_arquive(path):
    """
    Lê um arquivo e retorna uma lista com as linhas do arquivo.

    param path: Caminho do arquivo.
    """
    imports = []
    with open(path, "r", encoding="utf-8") as arqv:
        for line in arqv:
            imports.append(line.strip())

    return imports


def write_arquive(path, data):
    """
    Escreve em um arquivo.

    param path: Caminho do arquivo.
    param data: Dados a serem escritos.
    """
    data = pd.DataFrame(data.items(), columns=["x", "y"])
    with open(path, "w", encoding="utf-8") as arqv:
        arqv.write("Método de Heun\nTabela de valores:\n\n")
        arqv.write(data.to_string(index=False))


def f(x, y):
    """
    Retorna o valor da função f(x, y) no ponto (x, y).

    param x: Valor de x.
    param y: Valor de y.
    """
    _x = sp.symbols("x")
    _y = sp.symbols("y")

    _func = func.subs(_x, x)
    _func = _func.subs(_y, y)
    return _func


def heun_solution(x0, y0, h, n):
    """
    Resolve uma EDO de primeira ordem pelo método de Heun.
    Retorna um dicionário com os valores de x e y.

    param x0: Valor inicial de x.
    param y0: Valor inicial de y.
    param h: Tamanho do passo.
    param n: Quantidade de passos.
    """

    dots = {}
    dots[x0] = round(y0, 6)

    for _ in range(n):
        k1 = f(x0, y0)
        k2 = f(x0 + h, y0 + h * k1)
        
        y0 += (h / 2) * (k1 + k2)
        x0 += h
        dots[x0] = round(y0, 6)

    return dots


imports = read_arquive("heun/input.txt")
func = sp.sympify(imports[0]).evalf()

x0 = float(imports[1])
y0 = float(imports[2])
h = float(imports[3])
n = int(imports[4])

res = heun_solution(x0, y0, h, n)
write_arquive("heun/output.txt", res)
