"""Vista para cálculo de errores."""
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


@api_view(['POST'])
def calculo_error(request):
    """
    POST /api/calculos/error/
    Calcula el error absoluto, relativo y porcentual entre dos valores.
    """
    try:
        datos = request.data
        
        # Validar campos requeridos
        campos_requeridos = ['valor_verdadero', 'valor_aproximado']
        for campo in campos_requeridos:
            if campo not in datos:
                return Response(
                    {'error': f'El campo "{campo}" es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        valor_verdadero = float(datos['valor_verdadero'])
        valor_aproximado = float(datos['valor_aproximado'])
        
        # Calcular errores
        error_absoluto = abs(valor_verdadero - valor_aproximado)
        
        if valor_verdadero != 0:
            error_relativo = error_absoluto / abs(valor_verdadero)
            error_porcentual = error_relativo * 100
        else:
            error_relativo = float('inf') if error_absoluto != 0 else 0
            error_porcentual = float('inf') if error_absoluto != 0 else 0
        
        respuesta = {
            "valor_verdadero": valor_verdadero,
            "valor_aproximado": valor_aproximado,
            "error_absoluto": error_absoluto,
            "error_relativo": error_relativo,
            "error_porcentual": error_porcentual
        }
        
        return Response(respuesta, status=status.HTTP_200_OK)
        
    except ValueError as e:
        logger.error(f"ValueError en cálculo de error: {str(e)}")
        return Response(
            {'error': f'Error de validación: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error en cálculo de error: {str(e)}")
        return Response(
            {'error': f'Error en cálculo: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
