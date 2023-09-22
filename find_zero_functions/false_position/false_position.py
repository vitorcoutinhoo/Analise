# Importando a biblioteca sympy como sp para a manipulação de expressões algébricas
import sympy as sp

# Carregando os arquivos necessários na lista de importação
imports = []
with open("find_zero_functions/false_position/input.txt", "r", encoding="utf-8") as file:
    for line in file:
        imports.append(line.strip())

# Atribuindo os valores de entrada
a_value = float(imports[0])
b_value = float(imports[1])
error_value = float(imports[2])
function_string = imports[3]

# Retorna o valor da função no ponto x
def function(x_value):
    return sp.sympify(function_string).subs({"x": x_value}).evalf()

# Determina o zero na função por meio do método da posição falsa
def false_position(a_point, b_point):
    # Determinando os valores iniciais
    function_a = function(a_point)
    function_b = function(b_point)

    # Verificando se os valores iniciais são válidos
    if function_a * function_b > 0:
        print("No root in this interval")
        return
    
    # Loop para determinar o valor da raiz
    c_value = a_point
    function_c = function(c_value)
    while abs(function_c) > error_value:
        # Determinando o valor de c
        c_value = ((a_point * function_b) - (b_point * function_a)) / (function_b - function_a)
        function_c = function(c_value)
    
        if function_a * function_c < 0:
            b_point = c_value
        else:
            a_point = c_value

        function_a = function(a_point)
        function_b = function(b_point)

    return (f"{c_value:.5f} {function_c:.7f}")

# Escrevendo o resultado no arquivo de saída
with open("find_zero_functions/false_position/output.txt", "w", encoding="utf-8") as file:
    file.write(false_position(a_value, b_value))

    