"""
Serializadores para la Calculadora de Métodos Numéricos.
Convierten modelos Django a JSON y validan datos de entrada.
"""
from rest_framework import serializers
from .models import (
    Biseccion, NewtonRaphson, CambioDeBase, CalculoError, Polinomio,
    InterpolacionLagrange, DiferenciasNivel, AjusteCurvas, CalculoDerivada, Reporte
)


class BiseccionSerializer(serializers.ModelSerializer):
    """Serializador para el método de Bisección."""
    
    class Meta:
        model = Biseccion
        fields = [
            'id', 'expresion', 'a_inicial', 'b_inicial', 'tolerancia',
            'max_iteraciones', 'raiz_aproximada', 'iteraciones_realizadas',
            'historial_iteraciones', 'estado', 'descripcion', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'raiz_aproximada', 'iteraciones_realizadas', 
                           'historial_iteraciones', 'estado', 'fecha_creacion']


class NewtonRaphsonSerializer(serializers.ModelSerializer):
    """Serializador para el método de Newton-Raphson."""
    
    class Meta:
        model = NewtonRaphson
        fields = [
            'id', 'expresion', 'x_inicial', 'tolerancia', 'max_iteraciones',
            'raiz_aproximada', 'iteraciones_realizadas', 'historial_iteraciones',
            'estado', 'descripcion', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'raiz_aproximada', 'iteraciones_realizadas',
                           'historial_iteraciones', 'estado', 'fecha_creacion']


class CambioDeBaseSerializer(serializers.ModelSerializer):
    """Serializador para transformación de bases numéricas."""
    
    class Meta:
        model = CambioDeBase
        fields = [
            'id', 'numero_original', 'base_origen', 'base_destino',
            'numero_convertido', 'max_iteraciones', 'historial_pasos',
            'estado', 'descripcion', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'numero_convertido', 'historial_pasos',
                           'estado', 'fecha_creacion']


class CalculoErrorSerializer(serializers.ModelSerializer):
    """Serializador para cálculo de errores."""
    
    class Meta:
        model = CalculoError
        fields = [
            'id', 'valor_verdadero', 'valor_aproximado', 'error_absoluto',
            'error_relativo', 'error_porcentual', 'estado', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'error_absoluto', 'error_relativo',
                           'error_porcentual', 'estado', 'fecha_creacion']


class PolinomioSerializer(serializers.ModelSerializer):
    """Serializador para operaciones con polinomios."""
    
    class Meta:
        model = Polinomio
        fields = [
            'id', 'expresion', 'tipo_operacion', 'centro', 'grado',
            'punto_evaluacion', 'resultado_polinomio', 'coeficientes',
            'estado', 'descripcion', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'resultado_polinomio', 'coeficientes',
                           'estado', 'fecha_creacion']


class InterpolacionLagrangeSerializer(serializers.ModelSerializer):
    """Serializador para interpolación de Lagrange."""
    
    class Meta:
        model = InterpolacionLagrange
        fields = [
            'id', 'puntos_x', 'puntos_y', 'x_evaluacion', 'y_aproximado',
            'polinomio_resultado', 'coeficientes', 'error_interpolacion',
            'estado', 'descripcion', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'y_aproximado', 'polinomio_resultado',
                           'coeficientes', 'error_interpolacion', 'estado', 'fecha_creacion']


class DiferenciasNivelSerializer(serializers.ModelSerializer):
    """Serializador para diferencias divididas de Newton."""
    
    class Meta:
        model = DiferenciasNivel
        fields = [
            'id', 'puntos_x', 'puntos_y', 'x_evaluacion', 'y_aproximado',
            'tabla_diferencias', 'coeficientes', 'error_interpolacion',
            'estado', 'descripcion', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'y_aproximado', 'tabla_diferencias',
                           'coeficientes', 'error_interpolacion', 'estado', 'fecha_creacion']


class AjusteCurvasSerializer(serializers.ModelSerializer):
    """Serializador para ajuste de curvas."""
    
    class Meta:
        model = AjusteCurvas
        fields = [
            'id', 'puntos_x', 'puntos_y', 'tipo_ajuste', 'grado',
            'coeficientes', 'ecuacion_ajuste', 'r_cuadrado',
            'error_cuadratico_medio', 'desviacion_estandar',
            'estado', 'descripcion', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'coeficientes', 'ecuacion_ajuste',
                           'r_cuadrado', 'error_cuadratico_medio',
                           'desviacion_estandar', 'estado', 'fecha_creacion']


class CalculoDerivadaSerializer(serializers.ModelSerializer):
    """Serializador para cálculo de derivadas."""
    
    class Meta:
        model = CalculoDerivada
        fields = [
            'id', 'expresion', 'metodo', 'punto_evaluacion', 'h',
            'derivada_valor', 'derivada_expresion', 'segunda_derivada',
            'estado', 'descripcion', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'derivada_valor', 'derivada_expresion',
                           'segunda_derivada', 'estado', 'fecha_creacion']


class ReporteSerializer(serializers.ModelSerializer):
    """Serializador para reportes."""
    
    class Meta:
        model = Reporte
        fields = [
            'id', 'nombre', 'tipo_reporte', 'descripcion',
            'contenido_json', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'contenido', 'fecha_creacion']
