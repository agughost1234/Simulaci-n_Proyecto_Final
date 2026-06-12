"""Vista para Newton-Sistemas de Ecuaciones."""
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..services.newton_sistemas import NewtonSistemas

logger = logging.getLogger(__name__)


@api_view(['POST'])
def newton_sistemas_calcular(request):
    """
    POST /api/calculos/newton-sistemas/
    Resuelve un sistema de ecuaciones no lineales usando Newton.
    
    Parámetros esperados:
    {
        "ecuaciones": ["x**2 + y**2 - 4", "x - y"],
        "valores_iniciales": [1.0, 1.0],
        "tolerancia": 0.0001,
        "max_iteraciones": 100
    }
    """
    try:
        datos = request.data
        
        # Validar campos requeridos
        campos_requeridos = ['ecuaciones', 'valores_iniciales']
        for campo in campos_requeridos:
            if campo not in datos:
                return Response(
                    {'error': f'El campo "{campo}" es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        ecuaciones = datos['ecuaciones']
        valores_iniciales = datos['valores_iniciales']
        tolerancia = float(datos.get('tolerancia', 0.0001))
        max_iteraciones = int(datos.get('max_iteraciones', 100))
        
        # Validar que sean listas
        if not isinstance(ecuaciones, list) or not isinstance(valores_iniciales, list):
            return Response(
                {'error': 'ecuaciones y valores_iniciales deben ser arrays', 'success': False},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(ecuaciones) != len(valores_iniciales):
            return Response(
                {'error': f'Se esperan {len(ecuaciones)} valores iniciales', 'success': False},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear y ejecutar Newton-Sistemas
        metodo = NewtonSistemas(None, tolerancia, max_iteraciones)
        resultado = metodo.ejecutar(ecuaciones, valores_iniciales)
        
        # Verificar si hay error en la ejecución
        if 'error' in resultado:
            return Response(
                {'error': resultado['error'], 'success': False},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Agregar gráfica en base64 si existe
        resultado['grafica_png'] = metodo.grafica_base64 if metodo.grafica_base64 else None
        resultado['success'] = True
        
        return Response(resultado, status=status.HTTP_200_OK)
        
    except ValueError as e:
        logger.error(f"ValueError en Newton-Sistemas: {str(e)}")
        return Response(
            {'error': f'Error de validación: {str(e)}', 'success': False},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error en Newton-Sistemas: {str(e)}")
        return Response(
            {'error': f'Error en cálculo: {str(e)}', 'success': False},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
