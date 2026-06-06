"""
Vistas para la Calculadora de Métodos Numéricos.
Integra los módulos de Python numéricos con la API REST.
"""
import sys
import logging
from pathlib import Path
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import json

from .models import (
    Biseccion, NewtonRaphson, CambioDeBase, CalculoError, Polinomio,
    InterpolacionLagrange, DiferenciasNivel, AjusteCurvas, CalculoDerivada, Reporte
)
from .serializers import (
    BiseccionSerializer, NewtonRaphsonSerializer, CambioDeBaseSerializer,
    CalculoErrorSerializer, PolinomioSerializer, InterpolacionLagrangeSerializer,
    DiferenciasNivelSerializer, AjusteCurvasSerializer, CalculoDerivadaSerializer,
    ReporteSerializer
)

# Configurar logging
logger = logging.getLogger(__name__)

# Agregar el directorio de módulos al path
backend_path = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(backend_path))

# Importar módulos numéricos
try:
    from evaluador import Evaluador
    from biseccion import Biseccion as BiseccionMetodo
    from newton_raphson import NewtonRaphson as NewtonRaphsonMetodo
    from cambios_base import CambiosDeBase as CambiosDeBaseMetodo
    from metodo_numerico import MetodoNumerico
except ImportError as e:
    logger.warning(f"No se pudieron importar módulos numéricos: {e}")


class BiseccionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el método de Bisección.
    Endpoints:
    - POST /api/v1/biseccion/ : Crear nuevo cálculo
    - GET /api/v1/biseccion/ : Listar todos
    - GET /api/v1/biseccion/{id}/ : Obtener detalle
    - POST /api/v1/biseccion/calcular/ : Ejecutar cálculo
    """
    queryset = Biseccion.objects.all()
    serializer_class = BiseccionSerializer
    permission_classes = [AllowAny]
    ordering_fields = ['fecha_creacion', 'estado']
    search_fields = ['expresion', 'estado']
    
    @action(detail=False, methods=['post'], url_path='calcular')
    def calcular(self, request):
        """Endpoint para ejecutar un cálculo de Bisección."""
        try:
            expresion = request.data.get('expresion')
            a_inicial = float(request.data.get('a_inicial'))
            b_inicial = float(request.data.get('b_inicial'))
            tolerancia = float(request.data.get('tolerancia', 0.0001))
            max_iteraciones = int(request.data.get('max_iteraciones', 100))
            
            if not expresion:
                return Response(
                    {'error': 'La expresión es requerida'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Crear registro en la base de datos
            calc = Biseccion.objects.create(
                expresion=expresion,
                a_inicial=a_inicial,
                b_inicial=b_inicial,
                tolerancia=tolerancia,
                max_iteraciones=max_iteraciones,
                estado='pendiente'
            )
            
            # Ejecutar el cálculo
            try:
                evaluador = Evaluador(expresion)
                biseccion = BiseccionMetodo(evaluador, tolerancia, max_iteraciones)
                resultado = biseccion.ejecutar(a_inicial, b_inicial)
                
                if 'error' in resultado:
                    calc.estado = 'error'
                    calc.descripcion = resultado['error']
                    calc.save()
                    return Response(
                        {'error': resultado['error']},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Guardar resultados
                calc.raiz_aproximada = resultado['raiz']
                calc.iteraciones_realizadas = len(resultado['iteraciones'])
                calc.historial_iteraciones = resultado['iteraciones']
                calc.estado = resultado['estado']
                calc.save()
                
                serializer = self.get_serializer(calc)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                calc.estado = 'error'
                calc.descripcion = str(e)
                calc.save()
                logger.error(f"Error en bisección: {str(e)}")
                return Response(
                    {'error': f'Error en el cálculo: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except ValueError as e:
            return Response(
                {'error': f'Parámetro inválido: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error inesperado en bisección: {str(e)}")
            return Response(
                {'error': 'Error inesperado en el servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class NewtonRaphsonViewSet(viewsets.ModelViewSet):
    """ViewSet para el método de Newton-Raphson."""
    queryset = NewtonRaphson.objects.all()
    serializer_class = NewtonRaphsonSerializer
    permission_classes = [AllowAny]
    ordering_fields = ['fecha_creacion', 'estado']
    search_fields = ['expresion', 'estado']
    
    @action(detail=False, methods=['post'], url_path='calcular')
    def calcular(self, request):
        """Endpoint para ejecutar un cálculo de Newton-Raphson."""
        try:
            expresion = request.data.get('expresion')
            x_inicial = float(request.data.get('x_inicial'))
            tolerancia = float(request.data.get('tolerancia', 0.0001))
            max_iteraciones = int(request.data.get('max_iteraciones', 100))
            
            if not expresion:
                return Response(
                    {'error': 'La expresión es requerida'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            calc = NewtonRaphson.objects.create(
                expresion=expresion,
                x_inicial=x_inicial,
                tolerancia=tolerancia,
                max_iteraciones=max_iteraciones,
                estado='pendiente'
            )
            
            try:
                evaluador = Evaluador(expresion)
                newton = NewtonRaphsonMetodo(evaluador, tolerancia, max_iteraciones)
                resultado = newton.ejecutar(x_inicial)
                
                if 'error' in resultado:
                    calc.estado = 'error'
                    calc.descripcion = resultado['error']
                    calc.save()
                    return Response(
                        {'error': resultado['error']},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                calc.raiz_aproximada = resultado['raiz']
                calc.iteraciones_realizadas = len(resultado['iteraciones'])
                calc.historial_iteraciones = resultado['iteraciones']
                calc.estado = resultado['estado']
                calc.save()
                
                serializer = self.get_serializer(calc)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                calc.estado = 'error'
                calc.descripcion = str(e)
                calc.save()
                logger.error(f"Error en Newton-Raphson: {str(e)}")
                return Response(
                    {'error': f'Error en el cálculo: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except ValueError as e:
            return Response(
                {'error': f'Parámetro inválido: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error inesperado en Newton-Raphson: {str(e)}")
            return Response(
                {'error': 'Error inesperado en el servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CambiosDeBaseViewSet(viewsets.ModelViewSet):
    """ViewSet para transformación de bases numéricas."""
    queryset = CambioDeBase.objects.all()
    serializer_class = CambioDeBaseSerializer
    permission_classes = [AllowAny]
    ordering_fields = ['fecha_creacion', 'estado']
    search_fields = ['numero_original', 'estado']
    
    @action(detail=False, methods=['post'], url_path='calcular')
    def calcular(self, request):
        """Endpoint para convertir entre bases."""
        try:
            numero_original = request.data.get('numero_original')
            base_origen = int(request.data.get('base_origen'))
            base_destino = int(request.data.get('base_destino'))
            max_iteraciones = int(request.data.get('max_iteraciones', 15))
            
            if not numero_original:
                return Response(
                    {'error': 'El número es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            calc = CambioDeBase.objects.create(
                numero_original=numero_original,
                base_origen=base_origen,
                base_destino=base_destino,
                max_iteraciones=max_iteraciones,
                estado='pendiente'
            )
            
            try:
                conversor = CambiosDeBaseMetodo(None, None, max_iteraciones)
                resultado = conversor.ejecutar(base_origen, numero_original, base_destino)
                
                if isinstance(resultado, dict) and 'error' in resultado:
                    calc.estado = 'error'
                    calc.descripcion = resultado['error']
                    calc.save()
                    return Response(
                        {'error': resultado['error']},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                calc.numero_convertido = resultado
                calc.historial_pasos = conversor.historial
                calc.estado = 'exito'
                calc.save()
                
                serializer = self.get_serializer(calc)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                calc.estado = 'error'
                calc.descripcion = str(e)
                calc.save()
                logger.error(f"Error en cambio de base: {str(e)}")
                return Response(
                    {'error': f'Error en el cálculo: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except ValueError as e:
            return Response(
                {'error': f'Parámetro inválido: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error inesperado en cambio de base: {str(e)}")
            return Response(
                {'error': 'Error inesperado en el servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CalculoErrorViewSet(viewsets.ModelViewSet):
    """ViewSet para cálculo de errores."""
    queryset = CalculoError.objects.all()
    serializer_class = CalculoErrorSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='calcular')
    def calcular(self, request):
        """Endpoint para calcular errores."""
        try:
            valor_verdadero = float(request.data.get('valor_verdadero'))
            valor_aproximado = float(request.data.get('valor_aproximado'))
            
            # Cálculos de error
            error_absoluto = abs(valor_verdadero - valor_aproximado)
            if valor_verdadero != 0:
                error_relativo = error_absoluto / abs(valor_verdadero)
                error_porcentual = error_relativo * 100
            else:
                error_relativo = None
                error_porcentual = None
            
            calc = CalculoError.objects.create(
                valor_verdadero=valor_verdadero,
                valor_aproximado=valor_aproximado,
                error_absoluto=error_absoluto,
                error_relativo=error_relativo,
                error_porcentual=error_porcentual,
                estado='exito'
            )
            
            serializer = self.get_serializer(calc)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response(
                {'error': f'Parámetro inválido: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class PolinomioViewSet(viewsets.ModelViewSet):
    """ViewSet para operaciones con polinomios."""
    queryset = Polinomio.objects.all()
    serializer_class = PolinomioSerializer
    permission_classes = [AllowAny]
    ordering_fields = ['fecha_creacion', 'tipo_operacion']
    search_fields = ['expresion', 'tipo_operacion']


class InterpolacionLagrangeViewSet(viewsets.ModelViewSet):
    """ViewSet para interpolación de Lagrange."""
    queryset = InterpolacionLagrange.objects.all()
    serializer_class = InterpolacionLagrangeSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='calcular')
    def calcular(self, request):
        """Endpoint para interpolación de Lagrange."""
        return Response(
            {'error': 'Interpolación de Lagrange en desarrollo'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class DiferenciasNivelViewSet(viewsets.ModelViewSet):
    """ViewSet para diferencias divididas de Newton."""
    queryset = DiferenciasNivel.objects.all()
    serializer_class = DiferenciasNivelSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='calcular')
    def calcular(self, request):
        """Endpoint para diferencias divididas."""
        return Response(
            {'error': 'Diferencias divididas en desarrollo'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class AjusteCurvasViewSet(viewsets.ModelViewSet):
    """ViewSet para ajuste de curvas."""
    queryset = AjusteCurvas.objects.all()
    serializer_class = AjusteCurvasSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='calcular')
    def calcular(self, request):
        """Endpoint para ajuste de curvas."""
        return Response(
            {'error': 'Ajuste de curvas en desarrollo'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class CalculoDerivadaViewSet(viewsets.ModelViewSet):
    """ViewSet para cálculo de derivadas."""
    queryset = CalculoDerivada.objects.all()
    serializer_class = CalculoDerivadaSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='calcular')
    def calcular(self, request):
        """Endpoint para cálculo de derivadas."""
        try:
            expresion = request.data.get('expresion')
            punto_evaluacion = float(request.data.get('punto_evaluacion'))
            
            if not expresion:
                return Response(
                    {'error': 'La expresión es requerida'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            evaluador = Evaluador(expresion)
            derivada_valor = evaluador.evaluar_derivada(punto_evaluacion)
            
            calc = CalculoDerivada.objects.create(
                expresion=expresion,
                metodo='analitica',
                punto_evaluacion=punto_evaluacion,
                derivada_valor=derivada_valor,
                derivada_expresion=str(evaluador.f_prima),
                estado='exito'
            )
            
            serializer = self.get_serializer(calc)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response(
                {'error': f'Parámetro inválido: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
