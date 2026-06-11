"""Interpolacion con el polinomio de Lagrange."""

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


def lagrange_coefficients(x: Sequence[float], y: Sequence[float]) -> np.ndarray:
    """Calcula los coeficientes del polinomio interpolante en base monomial."""

    x_array, y_array = _validar_puntos(x, y)
    coefficients = np.zeros(x_array.size, dtype=float)

    for i in range(x_array.size):
        basis = np.array([1.0], dtype=float)
        denominator = 1.0

        for j in range(x_array.size):
            if i == j:
                continue
            basis = np.convolve(basis, np.array([1.0, -x_array[j]], dtype=float))
            denominator *= x_array[i] - x_array[j]

        coefficients += (y_array[i] / denominator) * basis

    return coefficients


def lagrange_evaluate(x: Sequence[float], y: Sequence[float], valor: float) -> float:
    """Evalua el polinomio de Lagrange en un punto."""

    coefficients = lagrange_coefficients(x, y)
    return float(np.polyval(coefficients, valor))


def lagrange_expression(x: Sequence[float], y: Sequence[float]) -> str:
    """Devuelve una representacion textual del polinomio de Lagrange."""

    x_array, y_array = _validar_puntos(x, y)
    terms = []

    for i in range(x_array.size):
        factor_terms = []
        denominator = 1.0

        for j in range(x_array.size):
            if i == j:
                continue
            factor_terms.append(f"(x - {x_array[j]:g})")
            denominator *= x_array[i] - x_array[j]

        numerator = " * ".join(factor_terms) if factor_terms else "1"
        terms.append(f"({y_array[i]:g} / {denominator:g}) * {numerator}")

    return "P(x) = " + " + ".join(terms)