"""Ejemplos de uso para los metodos implementados."""

from __future__ import annotations

import numpy as np

from backend import (
    divided_differences,
    lagrange_coefficients,
    lagrange_evaluate,
    newton_coefficients,
    newton_evaluate,
    newton_sistema_no_lineal,
)


def ejemplo_newton_sistemas() -> None:
    def f1(x: np.ndarray) -> float:
        return x[0] ** 2 + x[1] ** 2 - 4

    def f2(x: np.ndarray) -> float:
        return x[0] - x[1] - 1

    def j11(x: np.ndarray) -> float:
        return 2 * x[0]

    def j12(x: np.ndarray) -> float:
        return 2 * x[1]

    def j21(x: np.ndarray) -> float:
        return 1.0

    def j22(x: np.ndarray) -> float:
        return -1.0

    resultado = newton_sistema_no_lineal(
        funciones=[f1, f2],
        jacobiana=[[j11, j12], [j21, j22]],
        x0=[1.5, 0.5],
        tolerancia=1e-10,
        max_iteraciones=25,
    )

    print("Metodo de Newton para sistemas no lineales")
    print("Convergio:", resultado["convergio"])
    print("Solucion aproximada:", resultado["solucion"])
    print("Iteraciones:", resultado["iteraciones"])
    print("Residuo:", resultado["residuo"])
    print()


def ejemplo_lagrange() -> None:
    x = [1, 2, 3, 4]
    y = [1, 4, 9, 16]
    valor = 2.5

    coeficientes = lagrange_coefficients(x, y)

    print("Polinomio interpolante de Lagrange")
    print("Coeficientes:", coeficientes)
    print("Evaluacion en", valor, ":", lagrange_evaluate(x, y, valor))
    print()


def ejemplo_newton_interpolacion() -> None:
    x = [1, 2, 3, 4]
    y = [1, 4, 9, 16]
    valor = 2.5

    tabla = divided_differences(x, y)
    coeficientes = newton_coefficients(x, y)

    print("Diferencias divididas de Newton")
    print("Tabla:\n", tabla)
    print("Coeficientes:", coeficientes)
    print("Evaluacion en", valor, ":", newton_evaluate(x, coeficientes, valor))
    print()


def main() -> None:
    ejemplo_newton_sistemas()
    ejemplo_lagrange()
    ejemplo_newton_interpolacion()


if __name__ == "__main__":
    main()