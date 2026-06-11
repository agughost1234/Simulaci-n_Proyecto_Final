"""Serializador para transformación de bases numéricas."""
from rest_framework import serializers
from ..models import CambioDeBase


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
