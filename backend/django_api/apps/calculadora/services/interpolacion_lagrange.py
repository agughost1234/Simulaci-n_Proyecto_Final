"""Método de Interpolación de Lagrange."""
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from .metodo_numerico import MetodoNumerico


class InterpolacionLagrange(MetodoNumerico):
    """Interpolación polinómica de Lagrange."""
    
    def __init__(self, evaluador=None, tolerancia: float = 0.0001, max_iter: int = 100):
        super().__init__(evaluador, tolerancia, max_iter)
        self.grafica_base64 = None
    
    def ejecutar(self, puntos_x: list, puntos_y: list, x_eval: float):
        """
        Calcula la interpolación de Lagrange.
        
        Args:
            puntos_x: Lista de coordenadas x
            puntos_y: Lista de coordenadas y
            x_eval: Punto donde se evalúa
        
        Returns:
            dict con resultado de interpolación
        """
        try:
            self.limpiar_historial()
            
            puntos_x = np.array(puntos_x, dtype=float)
            puntos_y = np.array(puntos_y, dtype=float)
            n = len(puntos_x)
            
            # Calcular polinomio de Lagrange
            y_interp = 0
            for i in range(n):
                Li = 1
                for j in range(n):
                    if i != j:
                        Li *= (x_eval - puntos_x[j]) / (puntos_x[i] - puntos_x[j])
                
                y_interp += puntos_y[i] * Li
                
                self.historial.append({
                    'punto': i,
                    'x': puntos_x[i],
                    'y': puntos_y[i],
                    'Li': Li,
                    'aporte': puntos_y[i] * Li
                })
            
            respuesta = {
                "puntos_x": puntos_x.tolist(),
                "puntos_y": puntos_y.tolist(),
                "x_evaluacion": x_eval,
                "y_interpolado": float(y_interp),
                "grado_polinomio": n - 1,
                "historial": self.historial,
                "estado": "exito"
            }
            
            # Generar gráfica
            self._generar_grafica(puntos_x, puntos_y, x_eval, y_interp)
            
            return respuesta
            
        except Exception as e:
            return {"error": str(e)}
    
    def _generar_grafica(self, puntos_x, puntos_y, x_eval, y_interp):
        """Genera gráfica de interpolación."""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Puntos dados
            ax.scatter(puntos_x, puntos_y, color='red', s=100, label='Puntos dados', zorder=5)
            
            # Polinomio interpolante
            x_vals = np.linspace(min(puntos_x) - 1, max(puntos_x) + 1, 300)
            y_vals = []
            for x in x_vals:
                y = 0
                for i in range(len(puntos_x)):
                    Li = 1
                    for j in range(len(puntos_x)):
                        if i != j:
                            Li *= (x - puntos_x[j]) / (puntos_x[i] - puntos_x[j])
                    y += puntos_y[i] * Li
                y_vals.append(y)
            
            ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='Polinomio de Lagrange')
            
            # Punto evaluado
            ax.plot(x_eval, y_interp, 'g^', markersize=10, label=f'Interpolado ({x_eval:.3f}, {y_interp:.3f})')
            
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.set_title(f'Interpolación de Lagrange (Grado {len(puntos_x)-1})')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Convertir a base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            self.grafica_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close(fig)
            
        except Exception as e:
            print(f"Error generando gráfica: {str(e)}")
