from metodo_numerico import MetodoNumerico
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class Lagrange(MetodoNumerico):
    def __init__(self):
        super().__init__(evaluador=None, tolerancia=0.0, max_iter=0)

    def ejecutar(self, x_data: list, y_data: list):
        self.limpiar_historial()
        
        x_arr = np.array(x_data, dtype=float)
        y_arr = np.array(y_data, dtype=float)
        
        n = x_arr.size
        if n == 0 or n != y_arr.size:
            return {"error": "Las listas x e y deben tener el mismo tamaño."}
        if len(np.unique(x_arr)) != n:
            return {"error": "Los puntos de x deben ser completamente distintos."}
            
        coefficients = np.zeros(n, dtype=float)
        
        for i in range(n):
            basis = np.array([1.0], dtype=float)
            denominator = 1.0
            
            for j in range(n):
                if i == j:
                    continue
                basis = np.convolve(basis, np.array([1.0, -x_arr[j]], dtype=float))
                denominator *= x_arr[i] - x_arr[j]
                
            termino_L_i = (y_arr[i] / denominator) * basis
            coefficients += termino_L_i
            
            # Guardamos en el historial para mostrar en las tablas del Excel/Web
            self.historial.append({
                "polinomio_L_i": i,
                "x_i": x_arr[i],
                "y_i": y_arr[i],
                "denominador_L": denominator,
                "coef_monomial_parcial": str(termino_L_i.tolist())
            })
            
        self.coeficientes = coefficients
        self.x_data = x_arr
        self.y_data = y_arr
        
        return {
            "estado": "exito",
            "coeficientes": coefficients.tolist(), 
            "expresion": self._construir_expresion(),
            "historial": self.historial
        }

    def _construir_expresion(self):
        terms = []
        for i in range(self.x_data.size):
            factors = [f"(x - {self.x_data[j]:g})" for j in range(self.x_data.size) if i != j]
            den = 1.0
            for j in range(self.x_data.size):
                if i != j: den *= self.x_data[i] - self.x_data[j]
            coef = self.y_data[i] / den
            if coef != 0:
                terms.append(f"{coef:+g}*" + "*".join(factors))
        return " ".join(terms) if terms else "0"

    def graficar(self, nombre_imagen: str):
        if not hasattr(self, 'coeficientes'): return
        plt.figure(figsize=(10, 6))
        plt.scatter(self.x_data, self.y_data, color="red", label="Puntos Originales", zorder=5)
        
        x_vals = np.linspace(min(self.x_data) - 0.5, max(self.x_data) + 0.5, 200)
        y_vals = np.polyval(self.coeficientes, x_vals)
        
        plt.plot(x_vals, y_vals, color="blue", label="Polinomio de Lagrange")
        plt.title('Interpolación de Lagrange')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.savefig(f"{nombre_imagen}.png", bbox_inches='tight')
        plt.close()

    def obtener_grafica_base64(self):
        if not hasattr(self, 'coeficientes'): return ""
        plt.figure(figsize=(10, 6))
        plt.scatter(self.x_data, self.y_data, color="red", zorder=5)
        x_vals = np.linspace(min(self.x_data) - 0.5, max(self.x_data) + 0.5, 200)
        y_vals = np.polyval(self.coeficientes, x_vals)
        plt.plot(x_vals, y_vals, color="blue")
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        return base64.b64encode(buffer.read()).decode('utf-8')