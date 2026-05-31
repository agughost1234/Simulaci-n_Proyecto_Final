from sympy import diff, sympify, symbols, lambdify

class Evaluador:
    def __init__(self, expresion_str):
        self.x = symbols('x') # Definimos el símbolo 'x' para usar en la expresión
        expr_limpia = expresion_str.replace('^', '**') # Reemplazamos '^' por '**' para que sympy lo entienda como potencia
        self.expresion = sympify(expr_limpia) # Convertimos la cadena a una expresión simbólica de sympy
        self.f_num = lambdify(self.x, self.expresion, 'math') # Creamos una función numérica a partir de la expresión simbólica para evaluarla fácilmente
        self.f_prima = lambdify(self.x, diff(self.expresion, self.x), 'math') # Derivamos la expresión simbólica y creamos una función numérica para la derivada

    def evaluar(self, valor):
        return self.f_num(valor) # Evaluamos la función original en el valor dado

    def evaluar_derivada(self, valor):
        return self.f_prima(valor) # Evaluamos la primera derivada en el valor dado