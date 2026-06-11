"""Vista para cálculo de derivadas."""
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..services.evaluador import Evaluador

logger = logging.getLogger(__name__)


@api_view(['POST'])
def calculo_derivada(request):
    """
    POST /api/calculos/derivada/
    Calcula la derivada de una función en un punto.
    """
    try:
        datos = request.data
        
        # Validar campos requeridos
        campos_requeridos = ['expresion', 'punto_evaluacion']
        for campo in campos_requeridos:
            if campo not in datos:
                return Response(
                    {'error': f'El campo "{campo}" es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        expresion = datos['expresion']
        punto = float(datos['punto_evaluacion'])
        
        # Crear evaluador
        evaluador = Evaluador(expresion)
        
        # Evaluar derivada en el punto
        derivada_valor = evaluador.evaluar_derivada(punto)
        
        respuesta = {
            "expresion": expresion,
            "punto_evaluacion": punto,
            "derivada_valor": derivada_valor,
            "derivada_expresion": str(evaluador.f_prima)
        }
        
        return Response(respuesta, status=status.HTTP_200_OK)
        
    except ValueError as e:
        logger.error(f"ValueError en cálculo de derivada: {str(e)}")
        return Response(
            {'error': f'Error de validación: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error en cálculo de derivada: {str(e)}")
        return Response(
            {'error': f'Error en cálculo: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
