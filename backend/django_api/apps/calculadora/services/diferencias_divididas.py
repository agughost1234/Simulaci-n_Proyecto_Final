"""Método de Diferencias Divididas de Newton."""
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from .metodo_numerico import MetodoNumerico


class DiferenciasNivel(MetodoNumerico):
    """Interpolación por diferencias divididas de Newton."""
    
    def __init__(self, evaluador=None, tolerancia: float = 0.0001, max_iter: int = 100):
        super().__init__(evaluador, tolerancia, max_iter)
        self.grafica_base64 = None
        self.tabla_diferencias = []
    
    def ejecutar(self, puntos_x: list, puntos_y: list, x_eval: float):
        """
        Calcula interpolación por diferencias divididas de Newton.
        
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
            
            # Crear tabla de diferencias divididas
            tabla = np.zeros((n, n))
            tabla[:, 0] = puntos_y
            
            for j in range(1, n):
                for i in range(n - j):
                    tabla[i, j] = (tabla[i + 1, j - 1] - tabla[i, j - 1]) / (puntos_x[i + j] - puntos_x[i])
            
            self.tabla_diferencias = tabla.tolist()
            
            # Evaluar polinomio de Newton
            y_eval = tabla[0, 0]
            producto = 1
            for j in range(1, n):
                producto *= (x_eval - puntos_x[j - 1])
                y_eval += tabla[0, j] * producto
            
            # Crear historial
            for i in range(n):
                self.historial.append({
                    'punto': i,
                    'x': puntos_x[i],
                    'y': puntos_y[i],
                    'diferencias': [float(tabla[i, j]) if i + j < n else None for j in range(n)]
                })
            
            respuesta = {
                "polinomio": f"Polinomio de Newton (Diferencias Divididas) de grado {n - 1}",
                "puntos_x": puntos_x.tolist(),
                "puntos_y": puntos_y.tolist(),
                "x_evaluacion": x_eval,
                "y_interpolado": float(y_eval),
                "grado_polinomio": n - 1,
                "tabla_diferencias": self.tabla_diferencias,
                "historial": self.historial,
                "estado": "exito"
            }
            
            # Generar gráfica
            self._generar_grafica(puntos_x, puntos_y, x_eval, y_eval)
            
            return respuesta
            
        except Exception as e:
            return {"error": str(e)}
    
    def _generar_grafica(self, puntos_x, puntos_y, x_eval, y_eval):
        """Genera gráfica de interpolación."""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Puntos dados
            ax.scatter(puntos_x, puntos_y, color='red', s=100, label='Puntos dados', zorder=5)
            
            # Polinomio interpolante (Newton)
            x_vals = np.linspace(min(puntos_x) - 1, max(puntos_x) + 1, 300)
            y_vals = []
            n = len(puntos_x)
            tabla = np.zeros((n, n))
            tabla[:, 0] = puntos_y
            
            for j in range(1, n):
                for i in range(n - j):
                    tabla[i, j] = (tabla[i + 1, j - 1] - tabla[i, j - 1]) / (puntos_x[i + j] - puntos_x[i])
            
            for x in x_vals:
                y = tabla[0, 0]
                producto = 1
                for j in range(1, n):
                    producto *= (x - puntos_x[j - 1])
                    y += tabla[0, j] * producto
                y_vals.append(y)
            
            ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='Newton (Diferencias Divididas)')
            
            # Punto evaluado
            ax.plot(x_eval, y_eval, 'g^', markersize=10, label=f'Interpolado ({x_eval:.3f}, {y_eval:.3f})')
            
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.set_title(f'Interpolación por Diferencias Divididas (Grado {n-1})')
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
