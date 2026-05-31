from metodo_numerico import MetodoNumerico
import numpy as np
import matplotlib.pyplot as plt

class NewtonRaphson(MetodoNumerico):
    def ejecutar(self, x0: float):
        self.limpiar_historial()
        x_actual = x0

        self.historial.append({
            "iter": 0,
            "x_n": x_actual,
            "f_x_n": self.evaluador.evaluar(x_actual),
            "error": None
        })

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
    
    def graficar(self, nombre_imagen):
        if not self.historial:
            print("No hay datos")
            return   
        x_n = [it["x_n"] for it in self.historial]
        y_n = [it["f_x_n"] for it in self.historial]
        x_min = min(x_n)
        x_max = max(x_n)
        margen = (x_max - x_min) * 0.3
        if margen == 0: margen = 0.5
        x_inicial = x_min - margen
        x_final = x_max + margen
        x_vals = np.linspace(x_inicial, x_final, 200) 
        y_vals = [self.evaluador.evaluar(x) for x in x_vals]
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, label='f(x)', color='blue')
        plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
     
        plt.scatter(x_n, y_n, color="red", label="x_n", zorder=5)
        recta_tangente = lambda x,xn,yn,pendiente: pendiente * x - pendiente * xn + yn
        
        for i in range(len(x_n)):
            plt.vlines(x_n[i], 0, y_n[i], color="purple", linestyle=":", alpha=0.6)
            y_tangente = [recta_tangente(x, x_n[i], y_n[i], self.evaluador.evaluar_derivada(x_n[i])) for x in x_vals]
            etiqueta = "recta_tangente" if i == 0 else ""
            plt.plot(x_vals, y_tangente, label=etiqueta, color="orange")
        plt.scatter(x_n[-1], y_n[-1], color="green", label="Raíz Aproximada", zorder=5)
        #Ajustes visuales
        plt.xlim(x_inicial, x_final)
        plt.ylim(min(y_vals) * 1.5 - 0.02, max(y_vals) * 1.5 + 0.02)

        plt.title('Método de Newton Raphson', fontsize=14, pad=15)
        plt.xlabel('Eje x')
        plt.ylabel('Eje y')
        plt.grid(True, alpha=0.3)
        plt.legend()
        ruta_imagen = f'{nombre_imagen}.png'
        plt.savefig(ruta_imagen, bbox_inches='tight')
        plt.close()
        print(f"Gráfica guardada como {ruta_imagen}")

