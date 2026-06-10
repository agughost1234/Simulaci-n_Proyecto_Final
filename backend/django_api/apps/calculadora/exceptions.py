"""
Custom exception handlers y utilities para la API.
"""
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler que proporciona respuestas consistentes.
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        # Agregar timestamp y mensaje personalizado
        response.data = {
            'error': True,
            'message': str(response.data.get('detail', 'Error en la solicitud')),
            'status_code': response.status_code,
            'data': response.data if response.status_code != 400 else None
        }
        logger.error(f"API Error: {response.status_code} - {response.data}")
    
    return response


class APIException(Exception):
    """Excepción personalizada para la API."""
    
    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class CalculoException(APIException):
    """Excepción para errores en cálculos numéricos."""
    pass


class ValidationException(APIException):
    """Excepción para errores de validación."""
    pass
