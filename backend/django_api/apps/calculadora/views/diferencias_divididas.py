"""Vista para Diferencias Divididas de Newton."""
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..services.diferencias_divididas import DiferenciasNivel

logger = logging.getLogger(__name__)


@api_view(['POST'])
def diferencias_divididas_calcular(request):
    """
    POST /api/calculos/diferencias-divididas/
    Calcula interpolación por diferencias divididas de Newton.
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
        
        # Ejecutar diferencias divididas
        metodo = DiferenciasNivel()
        resultado = metodo.ejecutar(puntos_x, puntos_y, x_eval)
        
        if 'error' in resultado:
            return Response(resultado, status=status.HTTP_400_BAD_REQUEST)
        
        # Transformar respuesta para que sea compatible con frontend
        puntos = [{'x': float(x), 'y': float(y)} for x, y in zip(resultado.get('puntos_x', []), resultado.get('puntos_y', []))]
        resultado_transformado = {
            'polinomio': resultado.get('polinomio', 'Polinomio de Diferencias Divididas'),
            'puntos': puntos,
            'grafica_png': metodo.grafica_base64,
            'historial': resultado.get('historial', []),
            'estado': resultado.get('estado', 'exito')
        }
        
        return Response(resultado_transformado, status=status.HTTP_200_OK)
        
    except ValueError as e:
        logger.error(f"ValueError en Diferencias Divididas: {str(e)}")
        return Response(
            {'error': f'Error de validación: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error en Diferencias Divididas: {str(e)}")
        return Response(
            {'error': f'Error en cálculo: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
