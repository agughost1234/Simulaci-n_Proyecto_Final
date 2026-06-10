"""Serializador para reportes."""
from rest_framework import serializers
from ..models import Reporte


class ReporteSerializer(serializers.ModelSerializer):
    """Serializador para reportes."""
    
    class Meta:
        model = Reporte
        fields = [
            'id', 'nombre', 'tipo_reporte', 'descripcion',
            'contenido_json', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'contenido_json', 'fecha_creacion']
