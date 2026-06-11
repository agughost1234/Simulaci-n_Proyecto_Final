"""
Modelo: Método Iterativo de Jacobi
Resuelve sistemas de ecuaciones lineales usando el método iterativo de Jacobi.

El método de Jacobi divide la matriz A en su parte diagonal D y el resto R:
A = D + R

Fórmula iterativa:
x^(k+1) = D^(-1) · (b - R·x^(k))

Es útil para sistemas grandes y dispersos donde la matriz es diagonalmente dominante.
"""

from typing import List, Tuple, Dict
import math


def jacobi_method(
    A: List[List[float]],
    b: List[float],
    x0: List[float] = None,
    tol: float = 1e-6,
    max_iter: int = 100
) -> Dict:
    """
    Resuelve el sistema Ax = b usando el método de Jacobi.
    
    Args:
        A: Matriz de coeficientes n×n
        b: Vector de términos independientes
        x0: Aproximación inicial (si es None, usa vector cero)
        tol: Tolerancia para convergencia
        max_iter: Número máximo de iteraciones
    
    Returns:
        Dict con 'success', 'solution', 'iterations', 'error', 'history'
    """
    n = len(b)
    
    # Validaciones
    if len(A) != n or any(len(row) != n for row in A):
        raise ValueError(f"La matriz A debe ser {n}×{n}")
    
    # Verificar diagonal no nula
    for i in range(n):
        if abs(A[i][i]) < 1e-14:
            raise ValueError(f"El elemento diagonal A[{i}][{i}] es cero")
    
    # Inicializar x0 si no se proporciona
    if x0 is None:
        x = [0.0] * n
    else:
        if len(x0) != n:
            raise ValueError(f"x0 debe tener {n} elementos")
        x = x0.copy()
    
    history = []
    
    for iteration in range(max_iter):
        x_new = [0.0] * n
        
        # Calcular nueva aproximación
        for i in range(n):
            suma = b[i]
            for j in range(n):
                if j != i:
                    suma -= A[i][j] * x[j]
            x_new[i] = suma / A[i][i]
        
        # Calcular error (norma infinito de la diferencia)
        error = max(abs(x_new[i] - x[i]) for i in range(n))
        
        # Guardar historial (iteration + 1 para mostrar iteraciones desde 1)
        history.append({
            'iteration': iteration + 1,
            'x': x_new.copy(),
            'error': error
        })
        
        # Actualizar x
        x = x_new
        
        # Verificar convergencia
        if error < tol:
            return {
                'success': True,
                'solution': x,
                'iterations': iteration + 1,
                'error': error,
                'history': history,
                'message': f'Convergencia alcanzada en {iteration + 1} iteraciones'
            }
    
    # No convergió
    return {
        'success': False,
        'solution': x,
        'iterations': max_iter,
        'error': error,
        'history': history,
        'message': f'No convergió en {max_iter} iteraciones'
    }


def is_diagonally_dominant(A: List[List[float]], strict: bool = False) -> bool:
    """
    Verifica si una matriz es diagonalmente dominante.
    
    Una matriz es diagonalmente dominante si:
    |a_ii| >= Σ|a_ij| para todo i (no estricta)
    |a_ii| > Σ|a_ij| para todo i (estricta)
    
    Args:
        A: Matriz a verificar
        strict: Si True, verifica dominancia diagonal estricta
    
    Returns:
        True si la matriz es diagonalmente dominante
    """
    n = len(A)
    
    for i in range(n):
        diagonal = abs(A[i][i])
        suma_fila = sum(abs(A[i][j]) for j in range(n) if j != i)
        
        if strict:
            if diagonal <= suma_fila:
                return False
        else:
            if diagonal < suma_fila:
                return False
    
    return True


def format_jacobi_table(history: List[Dict]) -> List[List[str]]:
    """
    Formatea el historial para mostrar en tabla.
    
    Returns:
        Lista de listas con formato para tabla
    """
    if not history:
        return []
    
    n = len(history[0]['x'])
    table = []
    
    for record in history:
        iteration = record['iteration']
        x = record['x']
        error = record['error']
        
        row = [f"{iteration}"]
        row.extend([f"{xi:.6f}" for xi in x])
        row.append(f"{error:.2e}")
        
        table.append(row)
    
    return table


def create_sample_system() -> Tuple[List[List[float]], List[float], List[float]]:
    """
    Crea un sistema de ejemplo diagonalmente dominante.
    
    Sistema:
        10x₁ - x₂ + 2x₃ = 6
        -x₁ + 11x₂ - x₃ + 3x₄ = 25
        2x₁ - x₂ + 10x₃ - x₄ = -11
        3x₂ - x₃ + 8x₄ = 15
    
    Solución aproximada: [1, 2, -1, 1]
    """
    A = [
        [10.0, -1.0, 2.0, 0.0],
        [-1.0, 11.0, -1.0, 3.0],
        [2.0, -1.0, 10.0, -1.0],
        [0.0, 3.0, -1.0, 8.0]
    ]
    
    b = [6.0, 25.0, -11.0, 15.0]
    x0 = [0.0, 0.0, 0.0, 0.0]
    
    return A, b, x0


def validate_jacobi_input(
    n: int,
    matrix_entries: List[str],
    b_entries: List[str],
    x0_entries: List[str]
) -> Tuple[bool, str]:
    """
    Valida las entradas para el método de Jacobi.
    
    Returns:
        Tuple (es_valido, mensaje_error)
    """
    # Verificar número correcto de entradas
    expected_matrix = n * n
    if len(matrix_entries) != expected_matrix:
        return False, f"Se esperan {expected_matrix} entradas para la matriz {n}×{n}"
    
    if len(b_entries) != n:
        return False, f"Se esperan {n} entradas para el vector b"
    
    if len(x0_entries) != n:
        return False, f"Se esperan {n} valores iniciales"
    
    # Validar que sean números
    for i, val in enumerate(matrix_entries):
        if not val or not val.strip():
            return False, f"Entrada de matriz [{i}] vacía"
        try:
            float(val)
        except ValueError:
            return False, f"Entrada de matriz [{i}] = '{val}' no es un número válido"
    
    for i, val in enumerate(b_entries):
        if not val or not val.strip():
            return False, f"Entrada b[{i}] vacía"
        try:
            float(val)
        except ValueError:
            return False, f"Entrada b[{i}] = '{val}' no es un número válido"
    
    for i, val in enumerate(x0_entries):
        if not val or not val.strip():
            return False, f"Entrada x0[{i}] vacía"
        try:
            float(val)
        except ValueError:
            return False, f"Entrada x0[{i}] = '{val}' no es un número válido"
    
    return True, ""
