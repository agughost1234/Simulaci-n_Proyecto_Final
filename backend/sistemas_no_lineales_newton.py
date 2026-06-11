from metodo_numerico import MetodoNumerico
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class NewtonSistemas(MetodoNumerico):
    def __init__(self, tolerancia: float = 1e-8, max_iteraciones: int = 100):
        # Al ser multivariable no usamos el evaluador univariado, pasamos None
        super().__init__(evaluador=None, tolerancia=tolerancia, max_iter=max_iteraciones)
        
    def ejecutar(self, funciones: list, jacobiana: list, x0: list):
        self.limpiar_historial()
        
        x_actual = np.array(x0, dtype=float)
        
        # Guardar el estado inicial (Iteración 0)
        registro_inicial = {"iteracion": 0, "error": None, "residuo": None}
        for idx, val in enumerate(x_actual):
            registro_inicial[f"x_{idx}"] = val
        self.historial.append(registro_inicial)

        for iteracion in range(1, self.max_iter + 1):
            # Evaluamos el sistema de ecuaciones y la jacobiana
            valores = np.array([float(f(x_actual)) for f in funciones], dtype=float)
            jac = np.array([[float(f(x_actual)) for f in fila] for fila in jacobiana], dtype=float)

            try:
                delta = np.linalg.solve(jac, -valores)
            except np.linalg.LinAlgError:
                return {"error": "La matriz Jacobiana es singular en la iteración actual."}

            x_siguiente = x_actual + delta
            error = float(np.linalg.norm(delta, ord=np.inf))
            residuo = float(np.linalg.norm(valores, ord=np.inf))

            # Guardamos en el historial con columnas dinámicas para cada variable (x_0, x_1, ...)
            registro = {"iteracion": iteracion, "error": error, "residuo": residuo}
            for idx, val in enumerate(x_siguiente):
                registro[f"x_{idx}"] = val
            
            self.historial.append(registro)
            x_actual = x_siguiente

            # Criterio de parada
            if error < self.tol or residuo < self.tol:
                break

        # Almacenamos internamente las listas para el gráfico de convergencia
        self.iteraciones_grafica = [p["iteracion"] for p in self.historial if p["iteracion"] > 0]
        self.errores_grafica = [p["error"] for p in self.historial if p["error"] is not None]

        return {
            "estado": "exito" if iteracion <= self.max_iter else "max_iter_alcanzado",
            "solucion": x_actual.tolist(),
            "iteraciones": iteracion,
            "residuo": residuo,
            "historial": self.historial
        }

    