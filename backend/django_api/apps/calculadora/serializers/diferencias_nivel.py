"""Serializador para diferencias divididas de Newton."""
from rest_framework import serializers
from ..models import DiferenciasNivel


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
