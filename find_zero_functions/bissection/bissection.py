# Importando a biblioteca sympy como sp para a manipulação de expressões algébricas
import sympy as sp

# Carregando os arquivos necessários na lista de importação
imports = []
with open("find_zero_functions/bissection/input.txt", "r", encoding="utf-8") as file:
    for line in file:
        imports.append(line.strip())

# Atribuindo os valores de entrada
a_value = float(imports[0])
b_value = float(imports[1])
error_value = float(imports[2])
function_string = imports[3]

# Definindo máximo de iterações
# acrescenta 1 para tirar a configuração inicial
initial_error = b_value - a_value
max_iterations = round(float(sp.log(initial_error, 10) - sp.log(error_value, 10) / sp.log(2, 10)), 0) + 1 

# Retorna o valor da função no ponto x
def function(x_value):
    return sp.sympify(function_string).subs({"x": x_value}).evalf()

# Determina o zero na função por meio do método da bissecção
def bissection(a_point, b_point):
    # Contador de iterações
    count = 0

    # Determinando os valores iniciais
    function_a = function(a_point)
    function_b = function(b_point)

    # Verificando se os valores iniciais são válidos
    if function_a * function_b > 0:
        print("No root in this interval")
        return

    # Loop para determinar o valor da raiz
    while count < max_iterations:
        # Determinando o valor de c
        c_value = (a_point + b_point) / 2
        function_c = function(c_value)

        # Verificando se o valor de c é a raiz
        if function_c == 0 or float((b_point - a_point)) < error_value:
            # printa no arquivo de saída o número de iterações, o valor de c e o valor da função em c,
            # separados por um caractere de espaço
            return (f"{count} {c_value:.5f} {function_c:.7f}")

        # Incrementando o contador
        count += 1

        # Verificando se a raiz está no intervalo [a, c] ou [c, b]
        if function_a * function_c < 0:
            b_point = c_value
        else:
            a_point = c_value

    # Retorna se o número máximo de iterações foi atingido
    return "Max iterations reached"

# Escrevendo o resultado no arquivo de saída
with open("find_zero_functions/bissection/output.txt", "w", encoding="utf-8") as file:
    file.write(bissection(a_value, b_value))
