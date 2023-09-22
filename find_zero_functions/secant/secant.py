import sympy as sym

# Importando os valores do arquivo de entrada
imports = []
with open("find_zero_functions/secant/input.txt", "r", encoding="utf-8") as file:
    for line in file:
        imports.append(line.strip())

# Atribuindo os valores de entrada
x1_value = float(imports[0])
x2_value = float(imports[1])
error_value = float(imports[2])
function_string = imports[3]

# Retorna o valor da função no ponto x
def function(x_point):
    return sym.sympify(function_string).subs({"x": x_point}).evalf()

# Determina o zero na função por meio do método da secante
def secant(x1_point, x2_point):
    new_x = x2_point - ((function(x2_point) * (x2_point - x1_point)) / (function(x2_point) - function(x1_point)))

    while abs(function(new_x)) > error_value:
        x1_point = x2_point
        x2_point = new_x
        new_x = x2_point - ((function(x2_point) * (x2_point - x1_point)) / (function(x2_point) - function(x1_point)))
        
    return f"{new_x:.5f} {function(new_x):.7f}"

# mostra o resultado no arquivo de saída
with open("find_zero_functions/secant/output.txt", "w", encoding="utf-8") as file:
    file.write(secant(x1_value, x2_value))
