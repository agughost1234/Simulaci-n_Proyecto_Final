"""Serializador para Polinomio de Taylor."""
from rest_framework import serializers
from ..models import Polinomio


class PolinomioTaylorSerializer(serializers.ModelSerializer):
    """Serializador para Polinomio de Taylor."""
    
    class Meta:
        model = Polinomio
        fields = [
            'id', 'expresion', 'tipo_operacion', 'centro', 'grado',
            'punto_evaluacion', 'resultado_polinomio', 'coeficientes',
            'estado', 'descripcion', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'resultado_polinomio', 'coeficientes',
                           'estado', 'fecha_creacion']
