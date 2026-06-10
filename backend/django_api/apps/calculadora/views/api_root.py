"""Vista raíz de la API."""
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request):
    """Raíz de la API - Lista todos los endpoints disponibles."""
    endpoints = {
        "endpoints": {
            "biseccion": {
                "url": "/api/calculos/biseccion/",
                "metodo": "POST",
                "descripcion": "Método de Bisección para encontrar raíces"
            },
            "newton_raphson": {
                "url": "/api/calculos/newton-raphson/",
                "metodo": "POST",
                "descripcion": "Método de Newton-Raphson para encontrar raíces"
            },
            "cambios_base": {
                "url": "/api/calculos/cambios-base/",
                "metodo": "POST",
                "descripcion": "Conversión de números entre bases numéricas"
            },
            "error": {
                "url": "/api/calculos/error/",
                "metodo": "POST",
                "descripcion": "Cálculo de errores (absoluto, relativo, porcentual)"
            },
            "derivada": {
                "url": "/api/calculos/derivada/",
                "metodo": "POST",
                "descripcion": "Cálculo de derivadas en un punto"
            },
            "documentacion": {
                "url": "/api/docs/",
                "metodo": "GET",
                "descripcion": "Documentación interactiva Swagger"
            }
        }
    }
    return Response(endpoints)
