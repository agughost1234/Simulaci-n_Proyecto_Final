"""Interpolacion por diferencias divididas de Newton."""

from __future__ import annotations

from typing import Sequence

import numpy as np


def _validar_puntos(x: Sequence[float], y: Sequence[float]) -> tuple[np.ndarray, np.ndarray]:
    x_array = np.array(x, dtype=float)
    y_array = np.array(y, dtype=float)

    if x_array.size == 0:
        raise ValueError("Se requieren puntos de interpolacion.")

    if x_array.size != y_array.size:
        raise ValueError("x e y deben tener la misma cantidad de elementos.")

    if len(np.unique(x_array)) != x_array.size:
        raise ValueError("Los valores de x deben ser distintos.")

    return x_array, y_array


def divided_differences(x: Sequence[float], y: Sequence[float]) -> np.ndarray:
    """Construye la tabla de diferencias divididas."""

    x_array, y_array = _validar_puntos(x, y)
    n = x_array.size
    table = np.zeros((n, n), dtype=float)
    table[:, 0] = y_array

    for column in range(1, n):
        for row in range(n - column):
            numerator = table[row + 1, column - 1] - table[row, column - 1]
            denominator = x_array[row + column] - x_array[row]
            table[row, column] = numerator / denominator

    return table


def newton_coefficients(x: Sequence[float], y: Sequence[float]) -> np.ndarray:
    """Devuelve los coeficientes del polinomio de Newton."""

    table = divided_differences(x, y)
    return table[0, :]


def newton_evaluate(x: Sequence[float], coefficients: Sequence[float], valor: float) -> float:
    """Evalua el polinomio de Newton mediante multiplicacion anidada."""

    x_array = np.array(x, dtype=float)
    coef = np.array(coefficients, dtype=float)

    if x_array.size != coef.size:
        raise ValueError("x y los coeficientes deben tener la misma cantidad de elementos.")

    resultado = coef[-1]
    for indice in range(coef.size - 2, -1, -1):
        resultado = resultado * (valor - x_array[indice]) + coef[indice]

    return float(resultado)


def newton_expression(x: Sequence[float], coefficients: Sequence[float]) -> str:
    """Devuelve una representacion textual del polinomio de Newton."""

    x_array = np.array(x, dtype=float)
    coef = np.array(coefficients, dtype=float)

    if x_array.size != coef.size:
        raise ValueError("x y los coeficientes deben tener la misma cantidad de elementos.")

    terms = [f"{coef[0]:g}"]
    for i in range(1, coef.size):
        factors = " * ".join([f"(x - {x_array[j]:g})" for j in range(i)])
        terms.append(f"{coef[i]:g} * {factors}")

    return "P(x) = " + " + ".join(terms)