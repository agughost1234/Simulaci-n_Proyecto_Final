"""Vista para el método de Newton-Raphson."""
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..services.evaluador import Evaluador
from ..services.newton_raphson import NewtonRaphson

logger = logging.getLogger(__name__)


@api_view(['POST'])
def newton_raphson_calcular(request):
    """
    POST /api/calculos/newton-raphson/
    Calcula la raíz de una función usando el método de Newton-Raphson.
    """
    try:
        datos = request.data
        
        # Validar campos requeridos
        campos_requeridos = ['expresion', 'x_inicial']
        for campo in campos_requeridos:
            if campo not in datos:
                return Response(
                    {'error': f'El campo "{campo}" es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        expresion = datos['expresion']
        x_inicial = float(datos['x_inicial'])
        tolerancia = float(datos.get('tolerancia', 0.0001))
        max_iteraciones = int(datos.get('max_iteraciones', 100))
        
        # Crear evaluador y ejecutar Newton-Raphson
        evaluador = Evaluador(expresion)
        metodo = NewtonRaphson(evaluador, tolerancia, max_iteraciones)
        resultado = metodo.ejecutar(x_inicial)
        
        if 'error' in resultado:
            return Response(resultado, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(resultado, status=status.HTTP_200_OK)
        
    except ValueError as e:
        logger.error(f"ValueError en Newton-Raphson: {str(e)}")
        return Response(
            {'error': f'Error de validación: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error en Newton-Raphson: {str(e)}")
        return Response(
            {'error': f'Error en cálculo: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
