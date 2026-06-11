from .metodo_numerico import MetodoNumerico
import matplotlib.pyplot as plt
import numpy as np
import io
import base64


class Biseccion(MetodoNumerico):
    def __init__(self, evaluador, tolerancia: float = 0.0001, max_iter: int = 100):
        super().__init__(evaluador, tolerancia, max_iter)
        self.grafica_base64 = None
    
    def ejecutar(self, a: float, b: float):
        self.limpiar_historial()
        fa = self.evaluador.evaluar(a)
        fb = self.evaluador.evaluar(b)

        if fa * fb > 0:
            return {"error": "Bolzano no se cumple en [a, b]"}

        medio_anterior = None
        a_inicial = a
        b_inicial = b

        for i in range(1, self.max_iter + 1):
            medio = (a + b) / 2
            f_medio = self.evaluador.evaluar(medio)
            
            error_relativo = None
            if medio_anterior is not None:
                error_relativo = abs((medio - medio_anterior) / medio)

            self.historial.append({
                "iter": i, 
                "a": a, 
                "b": b, 
                "p_n": medio, 
                "f_p_n": f_medio,
                "error": error_relativo
            })

            if error_relativo is not None and error_relativo < self.tol:
                self._generar_grafica(a_inicial, b_inicial, medio)
                return {"raiz": medio, "iteraciones": self.historial, "estado": "exito"}

            if fa * f_medio < 0:
                b = medio
                fb = f_medio
            else:
                a = medio
                fa = f_medio
                
            medio_anterior = medio

        self._generar_grafica(a_inicial, b_inicial, medio)
        return {"raiz": medio, "iteraciones": self.historial, "estado": "max_iter_alcanzado"}
    
    def _generar_grafica(self, a, b, raiz):
        """Genera gráfica del método de bisección."""
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
            
            # Gráfica 1: Función y raíz
            x_vals = np.linspace(a - 0.5, b + 0.5, 300)
            y_vals = [self.evaluador.evaluar(x) for x in x_vals]
            
            ax1.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
            ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
            ax1.plot(raiz, self.evaluador.evaluar(raiz), 'r*', markersize=15, label=f'Raíz ≈ {raiz:.6f}')
            ax1.plot([a, b], [self.evaluador.evaluar(a), self.evaluador.evaluar(b)], 'go', markersize=8, label='Intervalo [a,b]')
            ax1.set_xlabel('x')
            ax1.set_ylabel('f(x)')
            ax1.set_title('Método de Bisección - Función')
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
            print(f"Error generando gráfica de bisección: {str(e)}")
