"""Vista para Interpolación de Lagrange."""
import logging
import base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..services.interpolacion_lagrange import InterpolacionLagrange

logger = logging.getLogger(__name__)


@api_view(['POST'])
def lagrange_calcular(request):
    """
    POST /api/calculos/interpolacion-lagrange/
    Calcula interpolación polinómica de Lagrange.
    """
    try:
        datos = request.data
        
        # Validar campos requeridos
        campos_requeridos = ['puntos_x', 'puntos_y', 'x_evaluacion']
        for campo in campos_requeridos:
            if campo not in datos:
                return Response(
                    {'error': f'El campo "{campo}" es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        puntos_x = list(map(float, datos['puntos_x']))
        puntos_y = list(map(float, datos['puntos_y']))
        x_eval = float(datos['x_evaluacion'])
        
        if len(puntos_x) != len(puntos_y):
            return Response(
                {'error': 'puntos_x y puntos_y deben tener la misma longitud'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ejecutar interpolación
        metodo = InterpolacionLagrange()
        resultado = metodo.ejecutar(puntos_x, puntos_y, x_eval)
        
        if 'error' in resultado:
            return Response(resultado, status=status.HTTP_400_BAD_REQUEST)
        
        # Agregar gráfica en base64
        resultado['grafica_png'] = metodo.grafica_base64
        
        return Response(resultado, status=status.HTTP_200_OK)
        
    except ValueError as e:
        logger.error(f"ValueError en Lagrange: {str(e)}")
        return Response(
            {'error': f'Error de validación: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error en Lagrange: {str(e)}")
        return Response(
            {'error': f'Error en cálculo: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
