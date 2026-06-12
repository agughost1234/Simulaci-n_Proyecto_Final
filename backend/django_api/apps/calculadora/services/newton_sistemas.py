"""Método de Newton para Sistemas de Ecuaciones."""
from .metodo_numerico import MetodoNumerico
from sympy import symbols, Matrix, lambdify, diff, sympify
import numpy as np
import matplotlib.pyplot as plt
import io
import base64


class NewtonSistemas(MetodoNumerico):
    """Newton para resolver sistemas de ecuaciones no lineales."""
    
    def __init__(self, evaluador=None, tolerancia: float = 0.0001, max_iter: int = 100):
        super().__init__(evaluador, tolerancia, max_iter)
        self.grafica_base64 = None
    
    def ejecutar(self, ecuaciones: list, valores_iniciales: list):
        """
        Resuelve un sistema de ecuaciones usando Newton multivariable.
        
        Args:
            ecuaciones: Lista de strings con las ecuaciones (ej: ["x**2 + y**2 - 4", "x - y"])
            valores_iniciales: Array de valores iniciales [x0, y0, ...]
        
        Returns:
            dict con solución, iteraciones y gráfica
        """
        try:
            self.limpiar_historial()
            n = len(ecuaciones)
            
            if len(valores_iniciales) != n:
                return {"error": f"Se esperan {n} valores iniciales, se recibieron {len(valores_iniciales)}"}
            
            # Crear símbolos
            vars_simbolos = symbols(f'x0:{n}')
            if n == 1:
                vars_simbolos = (vars_simbolos,)
            
            # Crear funciones simbólicas usando sympify
            ecuaciones_limpias = [eq.replace('^', '**') for eq in ecuaciones]
            F = []
            
            # Mapping de nombres de variables para sympify
            var_dict = {f'x{i}': var for i, var in enumerate(vars_simbolos)}
            var_dict.update({str(var): var for var in vars_simbolos})
            
            for eq in ecuaciones_limpias:
                # Reemplazar x, y, z con x0, x1, x2
                eq_procesada = eq
                for i in range(n):
                    if i < 26:  # Letras del alfabeto (x, y, z, ...)
                        letra = chr(120 + i)  # 120 es 'x' en ASCII
                        eq_procesada = eq_procesada.replace(letra, f'x{i}')
                
                # Usar sympify con el diccionario de variables
                expr = sympify(eq_procesada, locals=var_dict)
                F.append(expr)
            
            F_matrix = Matrix(F)
            
            # Calcular Jacobiano
            J_matrix = F_matrix.jacobian(vars_simbolos)
            
            # Compilar funciones
            F_func = lambdify(vars_simbolos, F_matrix, 'numpy')
            J_func = lambdify(vars_simbolos, J_matrix, 'numpy')
            
            # Inicializar
            x_actual = np.array(valores_iniciales, dtype=float)
            
            self.historial.append({
                "iter": 0,
                "solucion": x_actual.tolist(),
                "residuo": float(np.linalg.norm(np.array(F_func(*x_actual)).flatten())),
                "error": None
            })
            
            # Iteraciones de Newton
            for i in range(1, self.max_iter + 1):
                # Evaluar F y J en x_actual
                F_val = np.array(F_func(*x_actual)).flatten()
                J_val = np.array(J_func(*x_actual)).astype(float)
                
                residuo = np.linalg.norm(F_val)
                
                # Verificar singularidad de Jacobiano
                try:
                    det_J = np.linalg.det(J_val)
                    if abs(det_J) < 1e-10:
                        return {"error": "Jacobiano singular. No se puede continuar."}
                except:
                    return {"error": "Error al calcular el determinante del Jacobiano."}
                
                # Resolver: J(x) * delta = -F(x)
                try:
                    delta = np.linalg.solve(J_val, -F_val)
                except np.linalg.LinAlgError:
                    return {"error": "Error al resolver el sistema lineal en Newton."}
                
                x_siguiente = x_actual + delta
                error_norm = np.linalg.norm(x_siguiente - x_actual) / (np.linalg.norm(x_siguiente) + 1e-10)
                
                self.historial.append({
                    "iter": i,
                    "solucion": x_siguiente.tolist(),
                    "residuo": float(np.linalg.norm(np.array(F_func(*x_siguiente)).flatten())),
                    "error": float(error_norm)
                })
                
                if error_norm < self.tol:
                    self._generar_grafica(valores_iniciales, x_siguiente.tolist())
                    return {
                        "solucion": x_siguiente.tolist(),
                        "residuo": float(np.linalg.norm(np.array(F_func(*x_siguiente)).flatten())),
                        "iteraciones": self.historial,
                        "estado": "exito",
                        "grafica_png": self.grafica_base64
                    }
                
                x_actual = x_siguiente
            
            self._generar_grafica(valores_iniciales, x_actual.tolist())
            return {
                "solucion": x_actual.tolist(),
                "residuo": float(np.linalg.norm(np.array(F_func(*x_actual)).flatten())),
                "iteraciones": self.historial,
                "estado": "max_iter_alcanzado",
                "grafica_png": self.grafica_base64
            }
            
        except Exception as e:
            print(f"Error en Newton-Sistemas: {str(e)}")
            return {"error": str(e)}
    
    def _generar_grafica(self, x_inicial, x_final):
        """Genera gráfica de convergencia."""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Gráfica de convergencia
            iteraciones = [h['iter'] for h in self.historial]
            residuos = [h['residuo'] for h in self.historial]
            errores = [h['error'] if h['error'] is not None else 0 for h in self.historial]
            
            # Filtrar valores positivos para escala logarítmica
            iteraciones_log = []
            residuos_log = []
            errores_log = []
            
            for it, res, err in zip(iteraciones, residuos, errores):
                if res > 1e-15:
                    iteraciones_log.append(it)
                    residuos_log.append(res)
                    errores_log.append(max(err, 1e-15) if err > 0 else 1e-15)
            
            if iteraciones_log:
                ax.semilogy(iteraciones_log, residuos_log, 'b-o', linewidth=2, markersize=6, label='Residuo ||F(x)||')
                ax.semilogy(iteraciones_log, errores_log, 'r-s', linewidth=2, markersize=6, label='Error ||Δx||')
            
            ax.axhline(y=self.tol, color='g', linestyle='--', linewidth=2, label=f'Tolerancia = {self.tol}')
            
            ax.set_xlabel('Iteración', fontsize=12)
            ax.set_ylabel('Valor (escala logarítmica)', fontsize=12)
            ax.set_title('Convergencia - Newton para Sistemas', fontsize=14)
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3, which='both')
            
            plt.tight_layout()
            
            # Convertir a base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            self.grafica_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close(fig)
            
        except Exception as e:
            print(f"Error generando gráfica de Newton-Sistemas: {str(e)}")
