from metodo_numerico import MetodoNumerico
from sympy import diff, lambdify
import numpy as np
import matplotlib.pyplot as plt
import math
import io
import base64

class PolinomioTaylor(MetodoNumerico):
    def ejecutar(self, x0: float, x_eval: float, grado: int):
        self.limpiar_historial()
        x_sym = self.evaluador.x 
        expr_actual = self.evaluador.expresion 
        
        aprox_actual = 0
        
        for k in range(grado + 1):
            # Calcular la derivada k-ésima evaluada en x0
            if k == 0:
                deriv_k_num = float(expr_actual.subs(x_sym, x0)) # 
            else:
                expr_actual = diff(expr_actual, x_sym) 
                deriv_k_num = float(expr_actual.subs(x_sym, x0))
            
            # Calcular el término actual de la serie
            termino = (deriv_k_num / math.factorial(k)) * ((x_eval - x0) ** k)
            aprox_actual += termino
            
            # Guardar en el historial para generar Excel
            self.historial.append({
                "orden_k": k,
                "derivada_en_x0": deriv_k_num,
                "termino_k": termino,
                "aproximacion_acumulada": aprox_actual
            })
            
        self.grado = grado
        self.x0 = x0
        return {"aproximacion": aprox_actual, "historial": self.historial, "estado": "exito"}

    def graficar(self, nombre_imagen):
        if not self.historial:
            print("No hay datos")
            return
            
        # Rango de graficación centrado en x0
        x_vals = np.linspace(self.x0 - 5, self.x0 + 5, 200)
        y_real = [self.evaluador.evaluar(x) for x in x_vals]
        
        # Construir la función del polinomio de Taylor para graficar
        x_sym = self.evaluador.x
        expr_taylor = 0
        for item in self.historial:
            k = item["orden_k"]
            deriv_k = item["derivada_en_x0"]
            expr_taylor += (deriv_k / math.factorial(k)) * ((x_sym - self.x0) ** k)
            
        f_taylor = lambdify(x_sym, expr_taylor, 'math')
        y_taylor = [f_taylor(x) for x in x_vals]
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_real, label='Función Original f(x)', color='blue')
        plt.plot(x_vals, y_taylor, label=f'Polinomio de Taylor (Grado {self.grado})', color='orange', linestyle='--')
        
        # Punto de expansión
        y0 = self.evaluador.evaluar(self.x0)
        plt.scatter([self.x0], [y0], color='red', label=f'Punto de expansión x0={self.x0}', zorder=5)

        plt.title('Aproximación por Polinomio de Taylor', fontsize=14, pad=15)
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
        x_vals = np.linspace(self.x0 - 5, self.x0 + 5, 200)
        y_real = [self.evaluador.evaluar(x) for x in x_vals]
        
        x_sym = self.evaluador.x
        expr_taylor = 0
        for item in self.historial:
            k = item["orden_k"]
            expr_taylor += (item["derivada_en_x0"] / math.factorial(k)) * ((x_sym - self.x0) ** k)
            
        f_taylor = lambdify(x_sym, expr_taylor, 'math')
        y_taylor = [f_taylor(x) for x in x_vals]
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_real, color='blue')
        plt.plot(x_vals, y_taylor, color='orange', linestyle='--')
        plt.scatter([self.x0], [self.evaluador.evaluar(self.x0)], color='red', zorder=5)
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        return base64.b64encode(buffer.read()).decode('utf-8')