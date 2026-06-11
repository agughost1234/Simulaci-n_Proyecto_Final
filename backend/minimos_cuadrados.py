from metodo_numerico import MetodoNumerico
import matplotlib.pyplot as plt
import io
import base64

class MinimosCuadradosLineal(MetodoNumerico):
    def __init__(self):
        # Inicializamos la clase padre sin evaluador, tolerancia ni max_iter, 
        # ya que este es un método directo, no iterativo.
        super().__init__(evaluador=None, tolerancia=0.0, max_iter=0)
        
    def ejecutar(self, x_data: list, y_data: list):
        self.limpiar_historial()
        
        n = len(x_data)
        if n == 0 or n != len(y_data):
            return {"error": "Las listas de datos x e y deben tener el mismo tamaño y no estar vacías."}

        # Cálculo de las sumatorias necesarias
        sum_x = sum(x_data)
        sum_y = sum(y_data)
        sum_xy = sum(x * y for x, y in zip(x_data, y_data))
        sum_x2 = sum(x ** 2 for x in x_data)

        # Denominador de la fórmula de c1
        denominador = (n * sum_x2) - (sum_x ** 2)
        
        if denominador == 0:
            return {"error": "Todos los valores de x son iguales, no se puede ajustar una recta."}

        # Cálculo de coeficientes: y = c0 + c1*x
        c1 = ((n * sum_xy) - (sum_x * sum_y)) / denominador
        c0 = (sum_y / n) - (c1 * (sum_x / n))

        # Guardamos en el historial para la generación del Excel
        for i in range(n):
            y_pred = c0 + c1 * x_data[i]
            error_residual = abs(y_data[i] - y_pred)
            
            self.historial.append({
                "punto_i": i,
                "x_i": x_data[i],
                "y_real": y_data[i],
                "y_predicho": y_pred,
                "error_residual": error_residual
            })

        # Guardamos como atributos para graficar
        self.c0 = c0
        self.c1 = c1
        self.x_data = x_data
        self.y_data = y_data

        return {"c0": c0, "c1": c1, "historial": self.historial, "estado": "exito"}

    def graficar(self, nombre_imagen):
        if not self.historial:
            print("No hay datos en el historial.")
            return

        plt.figure(figsize=(10, 6))

        # Graficar los puntos de datos reales
        plt.scatter(self.x_data, self.y_data, color="red", label="Datos Reales", zorder=5)

        # Calcular los puntos extremos para trazar la línea recta ajustada
        x_min = min(self.x_data)
        x_max = max(self.x_data)
        margen = (x_max - x_min) * 0.1 if (x_max - x_min) > 0 else 0.5
        
        # Puntos inicial y final de la recta para que cubra todo el gráfico
        x_recta = [x_min - margen, x_max + margen]
        y_recta = [self.c0 + self.c1 * x for x in x_recta]

        # Ecuación formateada para la leyenda
        ecuacion_str = f"Ajuste Lineal: $y = {self.c0:.4f} + {self.c1:.4f}x$"
        plt.plot(x_recta, y_recta, color="blue", label=ecuacion_str)

        # Ajustes visuales de la gráfica
        plt.title('Ajuste por Mínimos Cuadrados (Modelo Lineal)', fontsize=14, pad=15)
        plt.xlabel('Eje x')
        plt.ylabel('Eje y')
        plt.grid(True, alpha=0.3)
        plt.legend()

        ruta_imagen = f'{nombre_imagen}.png'
        plt.savefig(ruta_imagen, bbox_inches='tight')
        plt.close()
        print(f"Gráfica guardada como {ruta_imagen}")


    def obtener_grafica_base64(self):
        if not self.historial: return ""
        plt.figure(figsize=(10, 6))
        plt.scatter(self.x_data, self.y_data, color="red", zorder=5)
        
        x_min, x_max = min(self.x_data), max(self.x_data)
        margen = (x_max - x_min) * 0.1 if (x_max - x_min) > 0 else 0.5
        x_recta = [x_min - margen, x_max + margen]
        y_recta = [self.c0 + self.c1 * x for x in x_recta]

        plt.plot(x_recta, y_recta, color="blue")
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        return base64.b64encode(buffer.read()).decode('utf-8')