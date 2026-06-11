"""Metodo de Newton para sistemas no lineales."""

from __future__ import annotations

from typing import Callable, Sequence

import numpy as np


FuncionSistema = Callable[[np.ndarray], float]
FuncionJacobiana = Sequence[Sequence[Callable[[np.ndarray], float]]]


def _evaluar_sistema(funciones: Sequence[FuncionSistema], x: np.ndarray) -> np.ndarray:
    return np.array([float(funcion(x)) for funcion in funciones], dtype=float)


def _evaluar_jacobiana(jacobiana: FuncionJacobiana, x: np.ndarray) -> np.ndarray:
    return np.array(
        [[float(funcion(x)) for funcion in fila] for fila in jacobiana],
        dtype=float,
    )


def newton_sistema_no_lineal(
    funciones: Sequence[FuncionSistema],
    jacobiana: FuncionJacobiana,
    x0: Sequence[float],
    tolerancia: float = 1e-8,
    max_iteraciones: int = 100,
) -> dict:
    """Resuelve un sistema no lineal con el metodo de Newton.

    Parameters
    ----------
    funciones:
        Lista de funciones f(x) que definen el sistema.
    jacobiana:
        Matriz de funciones derivadas parciales.
    x0:
        Vector inicial.
    tolerancia:
        Criterio de parada para el cambio entre iteraciones.
    max_iteraciones:
        Numero maximo de iteraciones.

    Returns
    -------
    dict
        Diccionario con la solucion, historial, convergencia y residuo.
    """

    if len(funciones) == 0:
        raise ValueError("Debe proporcionar al menos una funcion.")

    if len(jacobiana) != len(funciones):
        raise ValueError("La jacobiana debe tener la misma cantidad de filas que funciones.")

    dimension = len(x0)
    if any(len(fila) != dimension for fila in jacobiana):
        raise ValueError("La jacobiana debe ser una matriz cuadrada del mismo tamano que x0.")

    x_actual = np.array(x0, dtype=float)
    historial = []

    for iteracion in range(1, max_iteraciones + 1):
        valores = _evaluar_sistema(funciones, x_actual)
        jac = _evaluar_jacobiana(jacobiana, x_actual)

        try:
            delta = np.linalg.solve(jac, -valores)
        except np.linalg.LinAlgError as exc:
            raise ValueError("La jacobiana es singular en la iteracion actual.") from exc

        x_siguiente = x_actual + delta
        error = float(np.linalg.norm(delta, ord=np.inf))
        residuo = float(np.linalg.norm(valores, ord=np.inf))

        historial.append(
            {
                "iteracion": iteracion,
                "x": x_siguiente.copy(),
                "error": error,
                "residuo": residuo,
            }
        )

        x_actual = x_siguiente

        if error < tolerancia or residuo < tolerancia:
            return {
                "convergio": True,
                "solucion": x_actual,
                "iteraciones": iteracion,
                "residuo": residuo,
                "historial": historial,
            }

    valores_finales = _evaluar_sistema(funciones, x_actual)
    residuo_final = float(np.linalg.norm(valores_finales, ord=np.inf))

    return {
        "convergio": False,
        "solucion": x_actual,
        "iteraciones": max_iteraciones,
        "residuo": residuo_final,
        "historial": historial,
    }