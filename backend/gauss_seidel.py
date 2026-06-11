"""
Modelo: Método Iterativo de Gauss-Seidel

Implementación clásica del método de Gauss–Seidel para resolver sistemas
lineales Ax = b mediante actualizaciones en sitio (se usan los valores más
recientes conforme se actualizan las componentes de x).

Notas importantes sobre la implementación:
- El criterio de parada usado es el máximo cambio absoluto en una iteración
    (error = max_i |x_new_i - x_i|) comparado con `tol`.
- Se comprueba que la diagonal de A no contenga ceros para evitar divisiones
    por cero; no se fuerza ni verifica automáticamente condiciones suficientes
    para la convergencia (p. ej. diagonalmente dominante o SPD). Para matrices
    que no cumplan esas condiciones el método puede no converger.

Formato de salida (dict):
    - 'success': bool
    - 'solution': list[float]  (vector solución aproximado)
    - 'iterations': int       (número de iteraciones realizadas)
    - 'error': float          (error iterativo final = máximo cambio)
    - 'history': list[dict]   (cada elemento: {'iteration': int, 'x': list[float], 'error': float})
    - 'message': str

La función `format_gauss_seidel_table` convierte `history` en una tabla de
strings apta para mostrar en la interfaz.
"""
from typing import List, Dict, Tuple


def gauss_seidel_method(
    A: List[List[float]],
    b: List[float],
    x0: List[float] = None,
    tol: float = 1e-6,
    max_iter: int = 100
) -> Dict:
    """Ejecuta Gauss–Seidel sobre el sistema A x = b.

    Parámetros:
      - A: matriz cuadrada (lista de listas) de tamaño n×n
      - b: vector del lado derecho (longitud n)
      - x0: aproximación inicial (lista de longitud n), por defecto ceros
      - tol: tolerancia absoluta para el criterio de parada (error máximo)
      - max_iter: número máximo de iteraciones

    Retorna un diccionario con la información descrita en el docstring del
    módulo. El algoritmo actualiza `x` en sitio y guarda el historial de
    iteraciones en `history`.
    """
    n = len(b)
    if len(A) != n or any(len(row) != n for row in A):
        raise ValueError(f"La matriz A debe ser {n}×{n}")

    for i in range(n):
        if abs(A[i][i]) < 1e-14:
            raise ValueError(f"El elemento diagonal A[{i}][{i}] es cero")

    if x0 is None:
        x = [0.0] * n
    else:
        if len(x0) != n:
            raise ValueError(f"x0 debe tener {n} elementos")
        x = x0.copy()

    history = []

    for iteration in range(max_iter):
        error = 0.0
        for i in range(n):
            suma = b[i]
            for j in range(n):
                if j != i:
                    suma -= A[i][j] * x[j]
            x_new_i = suma / A[i][i]
            error = max(error, abs(x_new_i - x[i]))
            x[i] = x_new_i

        history.append({'iteration': iteration, 'x': x.copy(), 'error': error})

        if error < tol:
            return {
                'success': True,
                'solution': x,
                'iterations': iteration + 1,
                'error': error,
                'history': history,
                'message': f'Convergencia alcanzada en {iteration + 1} iteraciones'
            }

    return {
        'success': False,
        'solution': x,
        'iterations': max_iter,
        'error': error,
        'history': history,
        'message': f'No convergió en {max_iter} iteraciones'
    }


def format_gauss_seidel_table(history: List[Dict]) -> List[List[str]]:
    if not history:
        return []
    table = []
    for record in history:
        it = record['iteration']
        xs = record['x']
        err = record['error']
        row = [f"{it}"]
        row.extend([f"{v:.6f}" for v in xs])
        row.append(f"{err:.2e}")
        table.append(row)
    return table


def create_sample_system() -> Tuple[List[List[float]], List[float], List[float]]:
    A = [
        [4.0, -1.0, 0.0, 0.0],
        [-1.0, 4.0, -1.0, 0.0],
        [0.0, -1.0, 4.0, -1.0],
        [0.0, 0.0, -1.0, 3.0]
    ]
    b = [15.0, 10.0, 10.0, 10.0]
    x0 = [0.0, 0.0, 0.0, 0.0]
    return A, b, x0
