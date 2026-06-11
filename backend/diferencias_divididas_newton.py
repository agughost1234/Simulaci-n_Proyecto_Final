from metodo_numerico import MetodoNumerico
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class DiferenciasDivididasNewton(MetodoNumerico):
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
            return {"error": "Los puntos de x deben ser distintos."}

        # Construcción de la matriz matemática de diferencias divididas
        table = np.zeros((n, n), dtype=float)
        table[:, 0] = y_arr

        for column in range(1, n):
            for row in range(n - column):
                numerator = table[row + 1, column - 1] - table[row, column - 1]
                denominator = x_arr[row + column] - x_arr[row]
                table[row, column] = numerator / denominator

        # TRANSFORMAR LA MATRIZ A FILAS DE HISTORIAL PARA EL EXCEL/TABLA HTML
        for r in range(n):
            registro = {"i": r, "x_i": x_arr[r]}
            for c in range(n - r):
                registro[f"F_Orden_{c}"] = table[r, c]
            self.historial.append(registro)

        # Los coeficientes son la primera fila de la tabla
        self.coeficientes = table[0, :].tolist()
        self.x_data = x_arr
        self.y_data = y_arr

        return {
            "estado": "exito",
            "coeficientes": self.coeficientes,
            "expresion": self._construir_expresion(),
            "historial": self.historial
        }

    def _construir_expresion(self):
        terms = [f"{self.coeficientes[0]:g}"]
        for i in range(1, len(self.coeficientes)):
            if self.coeficientes[i] != 0:
                factors = " * ".join([f"(x - {self.x_data[j]:g})" for j in range(i)])
                terms.append(f"{self.coeficientes[i]:+g} * {factors}")
        return " ".join(terms)

    def evaluar_en_punto(self, valor: float) -> float:
        # Algoritmo de multiplicación anidada (Horner) para evaluar el polinomio
        resultado = self.coeficientes[-1]
        for i in range(len(self.coeficientes) - 2, -1, -1):
            resultado = resultado * (valor - self.x_data[i]) + self.coeficientes[i]
        return float(resultado)

    def graficar(self, nombre_imagen: str):
        if not hasattr(self, 'coeficientes'): return
        plt.figure(figsize=(10, 6))
        plt.scatter(self.x_data, self.y_data, color="red", label="Puntos dados", zorder=5)

        x_vals = np.linspace(min(self.x_data) - 0.5, max(self.x_data) + 0.5, 200)
        y_vals = [self.evaluar_en_punto(x) for x in x_vals]

        plt.plot(x_vals, y_vals, color="green", label="Polinomio de Newton")
        plt.title('Interpolación por Diferencias Divididas de Newton')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.savefig(f"{nombre_imagen}.png", bbox_inches='tight')
        plt.close()

    def obtener_grafica_base64(self):
        if not hasattr(self, 'coeficientes'): return ""
        plt.figure(figsize=(10, 6))
        plt.scatter(self.x_data, self.y_data, color="red", zorder=5)
        x_vals = np.linspace(min(self.x_data) - 0.5, max(self.x_data) + 0.5, 200)
        y_vals = [self.evaluar_en_punto(x) for x in x_vals]
        plt.plot(x_vals, y_vals, color="green")
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        return base64.b64encode(buffer.read()).decode('utf-8')