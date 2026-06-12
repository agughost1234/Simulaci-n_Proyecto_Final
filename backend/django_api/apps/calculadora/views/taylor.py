"""Vista para Polinomio de Taylor."""
import logging
import base64
import io
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..services.evaluador import Evaluador
from ..services.polinomio import Polinomio

logger = logging.getLogger(__name__)


@api_view(['POST'])
def polinomio_taylor_calcular(request):
    """
    POST /api/calculos/polinomio-taylor/
    Calcula la aproximación por serie de Taylor.
    """
    try:
        datos = request.data
        
        # Validar campos requeridos
        campos_requeridos = ['expresion', 'centro', 'grado', 'punto_evaluacion']
        for campo in campos_requeridos:
            if campo not in datos:
                return Response(
                    {'error': f'El campo "{campo}" es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        expresion = datos['expresion']
        centro = float(datos['centro'])
        grado = int(datos['grado'])
        punto_eval = float(datos['punto_evaluacion'])
        
        # Crear evaluador y ejecutar
        evaluador = Evaluador(expresion)
        metodo = Polinomio(evaluador)
        resultado = metodo.ejecutar(centro, grado, punto_eval)
        
        # Agregar gráfica en base64 y polinomio
        resultado['grafica_png'] = metodo.grafica_base64
        resultado['polinomio'] = resultado.get('polinomio', 'Polinomio de Taylor')
        resultado['success'] = True
        
        return Response(resultado, status=status.HTTP_200_OK)
        
    except ValueError as e:
        logger.error(f"ValueError en Taylor: {str(e)}")
        return Response(
            {'error': f'Error de validación: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error en Taylor: {str(e)}")
        return Response(
            {'error': f'Error en cálculo: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
