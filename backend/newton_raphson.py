from metodo_numerico import MetodoNumerico

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
