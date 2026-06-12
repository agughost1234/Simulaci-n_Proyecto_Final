"""Método de Polinomio de Taylor."""
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import math
from sympy import symbols, expand, series, diff
from .metodo_numerico import MetodoNumerico


class Polinomio(MetodoNumerico):
    """Aproximación por serie de Taylor."""
    
    def __init__(self, evaluador, tolerancia: float = 0.0001, max_iter: int = 100):
        super().__init__(evaluador, tolerancia, max_iter)
        self.grafica_base64 = None
    
    def ejecutar(self, centro: float, grado: int, punto_eval: float):
        """
        Calcula la serie de Taylor.
        
        Args:
            centro: Punto alrededor del cual se expande la serie
            grado: Orden del polinomio de Taylor
            punto_eval: Punto donde se evalúa la aproximación
        
        Returns:
            dict con resultados y gráfica en base64
        """
        try:
            self.limpiar_historial()
            
            # Obtener la serie de Taylor
            x = symbols('x')
            serie_taylor = series(
                self.evaluador.expresion, 
                (x, centro), 
                n=grado + 1
            ).removeO()
            
            # Evaluar en el punto
            valor_exacto = float(self.evaluador.evaluar(punto_eval))
            aproximacion = float(serie_taylor.subs(x, punto_eval))
            error = abs(valor_exacto - aproximacion)
            
            # Generar historial con estructura compatible con frontend
            self.historial = []
            aprox_acumulada = 0
            for i in range(grado + 1):
                derivada = diff(self.evaluador.expresion, x, i)
                derivada_en_centro = float(derivada.subs(x, centro))
                termino_k = (derivada_en_centro / math.factorial(i)) * ((punto_eval - centro) ** i)
                aprox_acumulada += termino_k
                
                self.historial.append({
                    'orden_k': i,
                    'derivada_en_x0': derivada_en_centro,
                    'termino_k': termino_k,
                    'aproximacion_acumulada': aprox_acumulada,
                })
            
            respuesta = {
                "aproximacion": aproximacion,
                "valor_exacto": valor_exacto,
                "error": error,
                "polinomio": str(serie_taylor),
                "historial": self.historial,
                "estado": "exito"
            }
            
            # Generar gráfica
            self._generar_grafica(punto_eval, centro, grado, valor_exacto, aproximacion)
            
            return respuesta
            
        except Exception as e:
            return {"error": str(e)}
    
    def _generar_grafica(self, punto_eval, centro, grado, valor_exacto, aproximacion):
        """Genera gráfica de la aproximación de Taylor."""
        print(f"DEBUG -> punto_eval={punto_eval}, valor_exacto={valor_exacto}, aproximacion={aproximacion}, tipo={type(aproximacion)}")
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Crear rango de puntos
            x_vals = np.linspace(centro - 2, centro + 2, 200)
            y_vals = [self.evaluador.evaluar(x) for x in x_vals]
            
            # Gráfica de función original
            ax.plot(x_vals, y_vals, 'b-', label='f(x) original', linewidth=2)
            
            # Puntos de evaluación
            ax.plot(punto_eval, valor_exacto, 'ro', markersize=8, label=f'f({punto_eval}) = {valor_exacto:.6f}')
            ax.plot(punto_eval, aproximacion, 'g^', markersize=8, label=f'Taylor({punto_eval}) = {aproximacion:.6f}')
            ax.plot(centro, self.evaluador.evaluar(centro), 'k*', markersize=12, label=f'Centro ({centro})')
            
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.set_title(f'Aproximación de Taylor - Grado {grado}')
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
