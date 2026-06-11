from sympy import diff, sympify, symbols, lambdify


class Evaluador:
    def __init__(self, expresion_str):
        self.x = symbols('x')
        expr_limpia = expresion_str.replace('^', '**')
        self.expresion = sympify(expr_limpia)
        self.f_num = lambdify(self.x, self.expresion, 'math')
        self.f_prima = lambdify(self.x, diff(self.expresion, self.x), 'math')

    def evaluar(self, valor):
        return self.f_num(valor)

    def evaluar_derivada(self, valor):
        return self.f_prima(valor)
