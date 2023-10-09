# importando as bibliotecas necessárias
import sympy as sym
from sympy import diff

# Carregando os arquivos necessários na lista de importação
imports = []
with open("find_zero_functions/newton_raphson/input.txt", "r", encoding="utf-8") as file:
    for line in file:
        imports.append(line.strip())

# Atribuindo os valores de entrada
x_value = float(imports[0])
error_value = float(imports[1])
function_string = imports[2]

# Retorna o valor da função no ponto x
def function(x_point):
    return sym.sympify(function_string).subs({"x": x_point}).evalf()

# Retorna o valor da derivada da função no ponto x
def derivative(x_point):
    return diff(sym.sympify(function_string), "x").subs({"x": x_point}).evalf()

# Determina o zero na função por meio do método de Newton-Raphson
def newton_raphson(x_point):
    count = 1
    new_x = x_point - (function(x_point) / derivative(x_point))

    while abs(function(new_x)) > error_value:
        x_point = new_x
        new_x = x_point - (function(x_point) / derivative(x_point))
        count += 1
        
    return (f"Número de iterações: {count}\n\nValor de x: {new_x:.5f}\nF(x): {function(new_x):.7f}")

# Resultado no arquivo de saida
with open("find_zero_functions/newton_raphson/output.txt", "w", encoding="utf-8") as file:
    file.write(f"{newton_raphson(x_value)}")
