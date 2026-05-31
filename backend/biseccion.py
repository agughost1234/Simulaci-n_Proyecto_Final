
from metodo_numerico import MetodoNumerico
import matplotlib.pyplot as plt
import numpy as np


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
    
    def graficar(self, nombre_imagen):
        if not self.historial:
            print("No hay datos para graficar.")
            return
        a_inicial = self.historial[0]['a']
        b_inicial = self.historial[0]['b']
        #se le da un poco de margen a los datos para que se vean mejor en la gráfica
        margen = (b_inicial - a_inicial) * 0.2
        x_min = a_inicial - margen
        x_max = b_inicial + margen
        #Generamos 200 puntos entre x_min y x_max para una gráfica suave
        x_vals = np.linspace(x_min, x_max, 200)
        y_vals = [self.evaluador.evaluar(x) for x in x_vals]
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, label='f(x)', color='blue')
        plt.axhline(0, color='black', linewidth=0.5, linestyle='--')

        p_n_vals = [it['p_n'] for it in self.historial]
        f_p_n_vals = [it['f_p_n'] for it in self.historial]
        plt.vlines(a_inicial, 0, self.evaluador.evaluar(a_inicial), color='purple', linestyle=':', alpha=0.6, label='a inicial')
        plt.vlines(b_inicial, 0, self.evaluador.evaluar(b_inicial), color='purple', linestyle=':', alpha=0.6, label='b inicial')
        plt.scatter(p_n_vals, f_p_n_vals, color='red', label='p_n', zorder=5)
        raiz_final, altura_final = self.historial[-1]['p_n'], self.historial[-1]['f_p_n']
        plt.scatter([raiz_final], [altura_final], color='green', s=100, label='Raíz Aproximada', zorder=6)
        plt.xlim(x_min, x_max)
        plt.title('Método de Bisección', fontsize=14, pad=15)
        plt.xlabel('Eje x')
        plt.ylabel('Eje y')
        plt.grid(True, alpha=0.3)
        plt.legend()
        ruta_imagen = f'{nombre_imagen}.png'
        plt.savefig(ruta_imagen, bbox_inches='tight')
        plt.close()
        print(f"Gráfica guardada como {ruta_imagen}")

