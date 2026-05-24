from sympy import sympify, symbols, lambdify

class Evaluador:
    def __init__(self, expresion_str):
        self.x = symbols('x')
        # Reemplazamos ^ por ** por si el usuario escribe x^2
        expr_limpia = expresion_str.replace('^', '**')
        self.expresion = sympify(expr_limpia)
        # Creamos una función rápida de Python
        self.f_num = lambdify(self.x, self.expresion, 'math')

    def evaluar(self, valor):
        return self.f_num(valor)