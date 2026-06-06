"""
Tests para la Calculadora API.
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Biseccion, NewtonRaphson, CambioDeBase


class BiseccionTestCase(TestCase):
    """Tests para el método de Bisección."""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_biseccion_create(self):
        """Test para crear un nuevo cálculo de bisección."""
        data = {
            'expresion': 'exp(-x) - x',
            'a_inicial': 0,
            'b_inicial': 1,
            'tolerancia': 0.0001,
            'max_iteraciones': 100
        }
        response = self.client.post('/api/v1/biseccion/calcular/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('raiz_aproximada', response.data)
    
    def test_biseccion_list(self):
        """Test para listar todos los cálculos."""
        response = self.client.get('/api/v1/biseccion/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CambioDeBaseTestCase(TestCase):
    """Tests para cambio de base."""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_cambio_base_binario_a_decimal(self):
        """Test para convertir de binario a decimal."""
        data = {
            'numero_original': '1011',
            'base_origen': 2,
            'base_destino': 10
        }
        response = self.client.post('/api/v1/cambios-base/calcular/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('numero_convertido', response.data)
