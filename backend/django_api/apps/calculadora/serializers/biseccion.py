"""Serializador para el método de Bisección."""
from rest_framework import serializers
from ..models import Biseccion


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
