"""Vista para Ajuste de Curvas."""
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..services.ajuste_curvas import AjusteCurvas

logger = logging.getLogger(__name__)


@api_view(['POST'])
def ajuste_curvas_calcular(request):
    """
    POST /api/calculos/ajuste-curvas/
    Calcula el ajuste de curvas por mínimos cuadrados.
    """
    try:
        datos = request.data
        
        # Validar campos requeridos
        campos_requeridos = ['puntos_x', 'puntos_y']
        for campo in campos_requeridos:
            if campo not in datos:
                return Response(
                    {'error': f'El campo "{campo}" es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        puntos_x = list(map(float, datos['puntos_x']))
        puntos_y = list(map(float, datos['puntos_y']))
        grado = int(datos.get('grado', 1))
        tipo_ajuste = datos.get('tipo_ajuste', 'polinomio')  # polinomio, exponencial, logaritmica
        
        if len(puntos_x) != len(puntos_y):
            return Response(
                {'error': 'puntos_x y puntos_y deben tener la misma longitud'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ejecutar ajuste
        metodo = AjusteCurvas()
        resultado = metodo.ejecutar(puntos_x, puntos_y, grado, tipo_ajuste)
        
        if 'error' in resultado:
            return Response(resultado, status=status.HTTP_400_BAD_REQUEST)
        
        # Transformar respuesta para que sea compatible con frontend
        puntos = [{'x': float(x), 'y': float(y)} for x, y in zip(resultado.get('puntos_x', []), resultado.get('puntos_y', []))]
        resultado_transformado = {
            'polinomio': resultado.get('ecuacion', f'Ajuste de grado {grado}'),
            'puntos': puntos,
            'grafica_png': metodo.grafica_base64,
            'historial': resultado.get('historial', []),
            'estado': resultado.get('estado', 'exito'),
            'r_cuadrado': resultado.get('r_cuadrado', 0)
        }
        
        return Response(resultado_transformado, status=status.HTTP_200_OK)
        
    except ValueError as e:
        logger.error(f"ValueError en Ajuste de Curvas: {str(e)}")
        return Response(
            {'error': f'Error de validación: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error en Ajuste de Curvas: {str(e)}")
        return Response(
            {'error': f'Error en cálculo: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
