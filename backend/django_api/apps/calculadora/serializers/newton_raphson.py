"""Serializador para el método de Newton-Raphson."""
from rest_framework import serializers
from ..models import NewtonRaphson


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
