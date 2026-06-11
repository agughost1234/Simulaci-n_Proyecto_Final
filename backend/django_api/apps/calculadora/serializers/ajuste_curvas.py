"""Serializador para ajuste de curvas."""
from rest_framework import serializers
from ..models import AjusteCurvas


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
