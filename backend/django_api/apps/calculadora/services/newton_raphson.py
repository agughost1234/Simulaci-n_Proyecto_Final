from .metodo_numerico import MetodoNumerico
import matplotlib.pyplot as plt
import numpy as np
import io
import base64


class NewtonRaphson(MetodoNumerico):
    def __init__(self, evaluador, tolerancia: float = 0.0001, max_iter: int = 100):
        super().__init__(evaluador, tolerancia, max_iter)
        self.grafica_base64 = None
    
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

            if dfx == 0:
                return {"error": "La derivada es cero. Newton-Raphson no puede continuar."}

            x_siguiente = x_actual - fx / dfx
            
            error = abs((x_siguiente - x_actual) / x_siguiente)

            self.historial.append({
                "iter": i,
                "x_n": x_siguiente,
                "f_x_n": self.evaluador.evaluar(x_siguiente),
                "error": error
            })

            if error < self.tol:
                self._generar_grafica(x0, x_siguiente)
                return {"raiz": x_siguiente, "iteraciones": self.historial, "estado": "exito"}

            x_actual = x_siguiente

        self._generar_grafica(x0, x_actual)
        return {"raiz": x_actual, "iteraciones": self.historial, "estado": "max_iter_alcanzado"}
    
    def _generar_grafica(self, x0, raiz):
        """Genera gráfica del método de Newton-Raphson."""
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
            
            # Gráfica 1: Función, derivada y raíz
            x_vals = np.linspace(x0 - 2, x0 + 2, 300)
            y_vals = [self.evaluador.evaluar(x) for x in x_vals]
            
            ax1.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
            ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
            ax1.plot(raiz, self.evaluador.evaluar(raiz), 'r*', markersize=15, label=f'Raíz ≈ {raiz:.6f}')
            ax1.plot(x0, self.evaluador.evaluar(x0), 'go', markersize=8, label=f'x₀ = {x0}')
            
            # Mostrar tangentes (primeras iteraciones)
            for i in range(min(3, len(self.historial) - 1)):
                x_i = self.historial[i]['x_n']
                fx_i = self.historial[i]['f_x_n']
                dfx_i = self.evaluador.evaluar_derivada(x_i)
                
                x_tan = np.linspace(x_i - 1, x_i + 1, 100)
                y_tan = fx_i + dfx_i * (x_tan - x_i)
                ax1.plot(x_tan, y_tan, '--', alpha=0.5, label=f'Tangente iter {i}')
            
            ax1.set_xlabel('x')
            ax1.set_ylabel('f(x)')
            ax1.set_title('Método de Newton-Raphson - Función')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Gráfica 2: Convergencia (error)
            iteraciones = [h['iter'] for h in self.historial]
            errores = [h['error'] if h['error'] is not None else 0 for h in self.historial]
            
            ax2.semilogy(iteraciones, errores, 'b-o', linewidth=2, markersize=4)
            ax2.axhline(y=self.tol, color='r', linestyle='--', label=f'Tolerancia = {self.tol}')
            ax2.set_xlabel('Iteración')
            ax2.set_ylabel('Error Relativo')
            ax2.set_title('Convergencia del Método')
            ax2.legend()
            ax2.grid(True, alpha=0.3, which='both')
            
            plt.tight_layout()
            
            # Convertir a base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            self.grafica_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close(fig)
            
        except Exception as e:
            print(f"Error generando gráfica de Newton-Raphson: {str(e)}")
