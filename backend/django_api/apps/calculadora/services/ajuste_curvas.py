"""Método de Ajuste de Curvas - Mínimos Cuadrados."""
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from .metodo_numerico import MetodoNumerico


class AjusteCurvas(MetodoNumerico):
    """Ajuste de curvas por mínimos cuadrados."""
    
    def __init__(self, evaluador=None, tolerancia: float = 0.0001, max_iter: int = 100):
        super().__init__(evaluador, tolerancia, max_iter)
        self.grafica_base64 = None
    
    def ejecutar(self, puntos_x: list, puntos_y: list, grado: int = 1, tipo_ajuste: str = 'polinomio'):
        """
        Calcula el ajuste de curvas.
        
        Args:
            puntos_x: Lista de coordenadas x
            puntos_y: Lista de coordenadas y
            grado: Grado del polinomio (default: 1 para lineal)
            tipo_ajuste: 'polinomio', 'exponencial', 'logaritmica'
        
        Returns:
            dict con coeficientes y estadísticas
        """
        try:
            self.limpiar_historial()
            
            puntos_x = np.array(puntos_x, dtype=float)
            puntos_y = np.array(puntos_y, dtype=float)
            n = len(puntos_x)
            
            if tipo_ajuste == 'polinomio':
                # Ajuste polinómico
                coeficientes = np.polyfit(puntos_x, puntos_y, grado)
                polinomio = np.poly1d(coeficientes)
                y_pred = polinomio(puntos_x)
                ecuacion = f"Polinomio de grado {grado}"
                
            elif tipo_ajuste == 'exponencial':
                # Ajuste exponencial: y = a * e^(bx)
                log_y = np.log(np.abs(puntos_y) + 1e-10)
                coef_lin = np.polyfit(puntos_x, log_y, 1)
                coeficientes = [np.exp(coef_lin[1]), coef_lin[0]]
                y_pred = coeficientes[0] * np.exp(coeficientes[1] * puntos_x)
                ecuacion = f"y = {coeficientes[0]:.6f} * e^({coeficientes[1]:.6f}*x)"
                
            elif tipo_ajuste == 'logaritmica':
                # Ajuste logarítmico: y = a + b*ln(x)
                log_x = np.log(puntos_x + 1e-10)
                coeficientes = np.polyfit(log_x, puntos_y, 1)
                y_pred = coeficientes[0] * log_x + coeficientes[1]
                ecuacion = f"y = {coeficientes[0]:.6f} + {coeficientes[1]:.6f}*ln(x)"
                
            else:
                return {"error": f"Tipo de ajuste '{tipo_ajuste}' no soportado"}
            
            # Calcular estadísticas
            residuos = puntos_y - y_pred
            ssr = np.sum(residuos ** 2)  # Suma de cuadrados residuales
            sst = np.sum((puntos_y - np.mean(puntos_y)) ** 2)  # Suma total de cuadrados
            r_cuadrado = 1 - (ssr / sst) if sst != 0 else 0
            error_cuadratico = np.sqrt(ssr / n)
            desviacion_estandar = np.std(residuos)
            
            # Crear historial
            for i in range(n):
                self.historial.append({
                    'punto': i,
                    'x': puntos_x[i],
                    'y_real': puntos_y[i],
                    'y_pred': y_pred[i],
                    'residuo': residuos[i],
                    'error_cuadrado': residuos[i] ** 2
                })
            
            respuesta = {
                "tipo_ajuste": tipo_ajuste,
                "grado": grado,
                "puntos_x": puntos_x.tolist(),
                "puntos_y": puntos_y.tolist(),
                "coeficientes": coeficientes.tolist() if isinstance(coeficientes, np.ndarray) else coeficientes,
                "ecuacion": ecuacion,
                "r_cuadrado": float(r_cuadrado),
                "error_cuadratico_medio": float(error_cuadratico),
                "desviacion_estandar": float(desviacion_estandar),
                "historial": self.historial,
                "estado": "exito"
            }
            
            # Generar gráfica
            self._generar_grafica(puntos_x, puntos_y, y_pred, ecuacion, r_cuadrado)
            
            return respuesta
            
        except Exception as e:
            return {"error": str(e)}
    
    def _generar_grafica(self, puntos_x, puntos_y, y_pred, ecuacion, r_cuadrado):
        """Genera gráfica del ajuste."""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Puntos reales
            ax.scatter(puntos_x, puntos_y, color='red', s=80, label='Datos reales', zorder=5)
            
            # Línea ajustada
            idx_ordenado = np.argsort(puntos_x)
            ax.plot(puntos_x[idx_ordenado], y_pred[idx_ordenado], 'b-', linewidth=2, label='Ajuste')
            
            # Líneas de residuos
            for i in range(len(puntos_x)):
                ax.plot([puntos_x[i], puntos_x[i]], [puntos_y[i], y_pred[i]], 'g--', alpha=0.5)
            
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.set_title(f'Ajuste de Curvas\n{ecuacion}\nR² = {r_cuadrado:.6f}')
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
