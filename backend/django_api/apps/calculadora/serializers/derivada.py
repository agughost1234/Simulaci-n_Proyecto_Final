"""Serializador para cálculo de derivadas."""
from rest_framework import serializers
from ..models import CalculoDerivada


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
