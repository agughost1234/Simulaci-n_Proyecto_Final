"""Serializador para interpolación de Lagrange."""
from rest_framework import serializers
from ..models import InterpolacionLagrange


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
