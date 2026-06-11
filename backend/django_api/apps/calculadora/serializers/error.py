"""Serializador para cálculo de errores."""
from rest_framework import serializers
from ..models import CalculoError


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
