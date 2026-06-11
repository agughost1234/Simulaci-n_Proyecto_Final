"""Vista para cambios de base."""
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..services.cambios_base import CambiosDeBase

logger = logging.getLogger(__name__)


@api_view(['POST'])
def cambios_base_calcular(request):
    """
    POST /api/calculos/cambios-base/
    Convierte un número entre diferentes bases numéricas.
    """
    try:
        datos = request.data
        
        # Validar campos requeridos
        campos_requeridos = ['numero', 'base_origen', 'base_destino']
        for campo in campos_requeridos:
            if campo not in datos:
                return Response(
                    {'error': f'El campo "{campo}" es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        numero = str(datos['numero'])
        base_origen = int(datos['base_origen'])
        base_destino = int(datos['base_destino'])
        max_iteraciones = int(datos.get('max_iteraciones', 50))
        
        # Crear instancia y ejecutar conversión
        conversor = CambiosDeBase(None, None, max_iteraciones)
        resultado_numero = conversor.ejecutar(base_origen, numero, base_destino)
        
        if isinstance(resultado_numero, dict) and 'error' in resultado_numero:
            return Response(resultado_numero, status=status.HTTP_400_BAD_REQUEST)
        
        respuesta = {
            "numero_original": numero,
            "base_origen": base_origen,
            "numero_convertido": resultado_numero,
            "base_destino": base_destino,
            "historial": conversor.historial
        }
        
        return Response(respuesta, status=status.HTTP_200_OK)
        
    except ValueError as e:
        logger.error(f"ValueError en cambio de base: {str(e)}")
        return Response(
            {'error': f'Error de validación: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error en cambio de base: {str(e)}")
        return Response(
            {'error': f'Error en cálculo: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
