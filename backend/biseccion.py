
from metodo_numerico import MetodoNumerico


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
