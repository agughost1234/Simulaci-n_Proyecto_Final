from sympy import sympify, symbols, lambdify, diff

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

class MetodoNumerico:
    def __init__(self, evaluador: Evaluador, tolerancia: float, max_iter: int):
        self.evaluador = evaluador
        self.tol = tolerancia
        self.max_iter = max_iter
        self.historial = []  

    def limpiar_historial(self):
        self.historial = []

class Biseccion(MetodoNumerico):
    def ejecutar(self, a: float, b: float):
        self.limpiar_historial()
        fa = self.evaluador.evaluar(a)
        fb = self.evaluador.evaluar(b)

        if fa * fb > 0:
            return {"error": "Bolzano no se cumple en [a, b]"}

        medio_anterior = None  # Para rastrear p_{n-1}

        for i in range(1, self.max_iter + 1):
            medio = (a + b) / 2  # p_n
            f_medio = self.evaluador.evaluar(medio)
            
            # Calcular el Error Relativo Aproximado si no es la primera iteración
            error_relativo = None
            if medio_anterior is not None:
                error_relativo = abs((medio - medio_anterior) / medio)

            # Guardamos exactamente las columnas de la tabla de clase
            self.historial.append({
                "iter": i, 
                "a": a, 
                "b": b, 
                "p_n": medio, 
                "f_p_n": f_medio,
                "error": error_relativo
            })
 # Criterio de parada exacto del examen: Error Relativo < Tolerancia
            if error_relativo is not None and error_relativo < self.tol:
                return {"raiz": medio, "iteraciones": self.historial, "estado": "exito"}

            if fa * f_medio < 0:
                b = medio
                fb = f_medio
            else:
                a = medio
                fa = f_medio
                
            # Guardamos el p_n actual para que sea el p_{n-1} en la próxima vuelta
            medio_anterior = medio

        return {"raiz": medio, "iteraciones": self.historial, "estado": "max_iter_alcanzado"}

class NewtonRaphson(MetodoNumerico):
    def ejecutar(self, x0: float):
        self.limpiar_historial()
        x_actual = x0

        for i in range(1, self.max_iter + 1):
            fx = self.evaluador.evaluar(x_actual)
            dfx = self.evaluador.evaluar_derivada(x_actual)

            # Evitar división por cero si la derivada es nula
            if dfx == 0:
                return {"error": "La derivada es cero. Newton-Raphson no puede continuar."}

            # Aplicamos la fórmula real
            x_siguiente = x_actual - fx / dfx
            
            # Error relativo 
            error = abs((x_siguiente - x_actual) / x_siguiente)

            self.historial.append({
                "iter": i,
                "x_n": x_siguiente,
                "f_x_n": self.evaluador.evaluar(x_siguiente),
                "error": error
            })

            if error < self.tol:
                return {"raiz": x_siguiente, "iteraciones": self.historial, "estado": "exito"}

            # Actualización clave para la siguiente iteración
            x_actual = x_siguiente

        return {"raiz": x_actual, "iteraciones": self.historial, "estado": "max_iter_alcanzado"}


    
# --- BLOQUE DE PRUEBA MANUAL (Ejemplo del Examen) ---
if __name__ == "__main__":
    # Probemos con el ejercicio de la imagen para validar que dé igual
    expresion = "exp(-x) - x" 
    tolerancia = 0.0001
    maximo_iteraciones = 100

    evaluador_test = Evaluador(expresion)
    busqueda_raiz = Biseccion(evaluador_test, tolerancia, maximo_iteraciones)
    
    resultado = busqueda_raiz.ejecutar(0, 1)

    if "error" in resultado:
        print(f"Error: {resultado['error']}")
    else:
        print(f"Estado de finalización: {resultado['estado'].upper()}")
        print(f"Raíz aproximada obtenida: {resultado['raiz']:.6f}\n")
        
        # Formato de tabla elegante e idéntico al solicitado
        print(f"{'n':<4} | {'an':<10} | {'bn':<10} | {'pn':<10} | {'f(pn)':<11} | {'ERROR':<10}")
        print("-" * 70)
        for it in resultado["iteraciones"]:
            err_str = f"{it['error']:<10.6f}" if it['error'] is not None else f"{'.....':<10}"
            print(f"{it['iter']:<4} | {it['a']:<10.6f} | {it['b']:<10.6f} | {it['p_n']:<10.6f} | {it['f_p_n']:<11.6f} | {err_str}")
        
        # Al final de tu código de prueba, puedes agregar esto:
    print("\n" + "="*50 + "\nProbando Newton-Raphson:\n" + "="*50)
    metodo_newton = NewtonRaphson(evaluador_test, tolerancia, maximo_iteraciones)
    res_newton = metodo_newton.ejecutar(0.5)

    print(f"Estado: {res_newton['estado'].upper()}")
    print(f"Raíz obtenida: {res_newton['raiz']:.6f}\n")
    print(f"{'n':<4} | {'xn':<10} | {'f(xn)':<11} | {'ERROR':<10}")
    print("-" * 45)
    for it in res_newton["iteraciones"]:
        print(f"{it['iter']:<4} | {it['x_n']:<10.6f} | {it['f_x_n']:<11.6f} | {it['error']:<10.6f}")