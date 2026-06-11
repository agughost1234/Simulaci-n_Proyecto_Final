"""
Servicios de cálculo y utilidades para métodos numéricos.
"""
import logging
import json
from datetime import datetime
from sympy import sympify, symbols, diff, lambdify
import numpy as np

logger = logging.getLogger(__name__)


class CalculoService:
    """Servicio base para cálculos numéricos."""
    
    @staticmethod
    def validar_expresion(expresion_str):
        """
        Valida que una expresión matemática sea válida.
        
        Args:
            expresion_str: String con la expresión
            
        Returns:
            Expresión sympy si es válida, raises ValueError si no
        """
        try:
            x = symbols('x')
            expr_limpia = expresion_str.replace('^', '**')
            expresion = sympify(expr_limpia)
            return expresion
        except Exception as e:
            logger.error(f"Expresión inválida: {expresion_str} - {str(e)}")
            raise ValueError(f"Expresión matemática inválida: {str(e)}")
    
    @staticmethod
    def validar_parametros(**kwargs):
        """
        Valida que los parámetros numéricos sean válidos.
        
        Args:
            **kwargs: Parámetros a validar
            
        Returns:
            Diccionario con parámetros validados
        """
        validados = {}
        
        for key, value in kwargs.items():
            if value is None:
                continue
                
            if isinstance(value, str) and value.isdigit():
                validados[key] = int(value)
            elif isinstance(value, str):
                try:
                    validados[key] = float(value)
                except ValueError:
                    validados[key] = value
            else:
                validados[key] = value
        
        return validados
    
    @staticmethod
    def calcular_errores(valor_verdadero, valor_aproximado):
        """
        Calcula error absoluto, relativo y porcentual.
        
        Returns:
            Diccionario con los tres tipos de error
        """
        error_absoluto = abs(valor_verdadero - valor_aproximado)
        
        if valor_verdadero != 0:
            error_relativo = error_absoluto / abs(valor_verdadero)
            error_porcentual = error_relativo * 100
        else:
            error_relativo = None
            error_porcentual = None
        
        return {
            'error_absoluto': error_absoluto,
            'error_relativo': error_relativo,
            'error_porcentual': error_porcentual
        }


class ReporteService:
    """Servicio para generar reportes."""
    
    @staticmethod
    def generar_reporte_json(datos, titulo="Reporte"):
        """Genera un reporte en formato JSON."""
        return {
            'titulo': titulo,
            'fecha_generacion': datetime.now().isoformat(),
            'datos': datos
        }
    
    @staticmethod
    def generar_reporte_tabla(datos_lista, columnas):
        """
        Genera una tabla formateada.
        
        Args:
            datos_lista: Lista de diccionarios con los datos
            columnas: Lista de nombres de columnas
            
        Returns:
            String con tabla formateada
        """
        # Calcular anchos de columna
        anchos = {col: len(col) for col in columnas}
        
        for fila in datos_lista:
            for col in columnas:
                valor = str(fila.get(col, ''))
                anchos[col] = max(anchos[col], len(valor))
        
        # Construir tabla
        linea_separadora = '+' + '+'.join('-' * (ancho + 2) for ancho in anchos.values()) + '+'
        linea_encabezado = '| ' + ' | '.join(
            col.ljust(anchos[col]) for col in columnas
        ) + ' |'
        
        tabla = [linea_separadora, linea_encabezado, linea_separadora]
        
        for fila in datos_lista:
            linea_datos = '| ' + ' | '.join(
                str(fila.get(col, '')).ljust(anchos[col]) for col in columnas
            ) + ' |'
            tabla.append(linea_datos)
        
        tabla.append(linea_separadora)
        
        return '\n'.join(tabla)


class ExportService:
    """Servicio para exportar datos."""
    
    @staticmethod
    def exportar_a_json(datos):
        """Exporta datos a JSON."""
        return json.dumps(datos, indent=2, ensure_ascii=False, default=str)
    
    @staticmethod
    def exportar_a_csv(datos_lista, columnas):
        """Exporta datos a CSV."""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=columnas)
        writer.writeheader()
        writer.writerows(datos_lista)
        
        return output.getvalue()
