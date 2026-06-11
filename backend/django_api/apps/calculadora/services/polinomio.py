"""Método de Polinomio de Taylor."""
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
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
                self.evaluador.f, 
                (x, centro), 
                n=grado + 1
            ).removeO()
            
            # Evaluar en el punto
            valor_exacto = float(self.evaluador.evaluar(punto_eval))
            valor_taylor = float(serie_taylor.subs(x, punto_eval))
            error = abs(valor_exacto - valor_taylor)
            
            # Generar historial con derivadas
            self.historial = []
            for i in range(grado + 1):
                derivada = diff(self.evaluador.f, x, i)
                valor_derivada = float(derivada.subs(x, centro))
                coef = valor_derivada / (1 if i == 0 else np.prod([j for j in range(1, i + 1)]))
                
                self.historial.append({
                    'orden': i,
                    'coeficiente': coef,
                    'derivada_en_centro': valor_derivada,
                })
            
            respuesta = {
                "centro": centro,
                "grado": grado,
                "punto_evaluacion": punto_eval,
                "valor_exacto": valor_exacto,
                "valor_taylor": valor_taylor,
                "error": error,
                "polinomio": str(serie_taylor),
                "historial": self.historial,
                "estado": "exito"
            }
            
            # Generar gráfica
            self._generar_grafica(punto_eval, centro, grado, valor_exacto, valor_taylor)
            
            return respuesta
            
        except Exception as e:
            return {"error": str(e)}
    
    def _generar_grafica(self, punto_eval, centro, grado, valor_exacto, valor_taylor):
        """Genera gráfica de la aproximación de Taylor."""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Crear rango de puntos
            x_vals = np.linspace(centro - 2, centro + 2, 200)
            y_vals = [self.evaluador.evaluar(x) for x in x_vals]
            
            # Gráfica de función original
            ax.plot(x_vals, y_vals, 'b-', label='f(x) original', linewidth=2)
            
            # Puntos de evaluación
            ax.plot(punto_eval, valor_exacto, 'ro', markersize=8, label=f'f({punto_eval}) = {valor_exacto:.6f}')
            ax.plot(punto_eval, valor_taylor, 'g^', markersize=8, label=f'Taylor({punto_eval}) = {valor_taylor:.6f}')
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
