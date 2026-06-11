"""Vista para exportar datos a Excel."""
import logging
import base64
import io
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


@api_view(['POST'])
def exportar_excel(request):
    """
    POST /api/calculos/exportar-excel/
    Convierte datos a archivo Excel y lo retorna como base64.
    
    Body:
    {
        "titulo": "Reporte Bisección",
        "datos": [
            {"iter": 1, "a": 0, "b": 1, "p_n": 0.5, "f_p_n": 0.1},
            ...
        ]
    }
    """
    try:
        datos = request.data
        
        if 'datos' not in datos:
            return Response(
                {'error': 'El campo "datos" es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        titulo = datos.get('titulo', 'Reporte')
        lista_datos = datos['datos']
        
        if not isinstance(lista_datos, list) or len(lista_datos) == 0:
            return Response(
                {'error': 'datos debe ser una lista no vacía'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear DataFrame
        df = pd.DataFrame(lista_datos)
        
        # Guardar en buffer
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Datos', index=False)
        
        buffer.seek(0)
        excel_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        respuesta = {
            "titulo": titulo,
            "filas": len(lista_datos),
            "columnas": list(df.columns),
            "excel_base64": excel_base64,
            "nombre_archivo": f"{titulo.replace(' ', '_')}.xlsx"
        }
        
        return Response(respuesta, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error exportando Excel: {str(e)}")
        return Response(
            {'error': f'Error al generar Excel: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def exportar_multiplos_excel(request):
    """
    POST /api/calculos/exportar-multiplos-excel/
    Crea un Excel con múltiples hojas.
    
    Body:
    {
        "hojas": [
            {
                "nombre": "Iteraciones",
                "datos": [...]
            },
            {
                "nombre": "Estadísticas",
                "datos": [...]
            }
        ]
    }
    """
    try:
        datos = request.data
        
        if 'hojas' not in datos:
            return Response(
                {'error': 'El campo "hojas" es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        hojas = datos['hojas']
        
        if not isinstance(hojas, list) or len(hojas) == 0:
            return Response(
                {'error': 'hojas debe ser una lista no vacía'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear Excel con múltiples hojas
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            for hoja in hojas:
                nombre = hoja.get('nombre', 'Hoja')
                lista_datos = hoja.get('datos', [])
                
                if lista_datos:
                    df = pd.DataFrame(lista_datos)
                    df.to_excel(writer, sheet_name=nombre, index=False)
        
        buffer.seek(0)
        excel_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        respuesta = {
            "cantidad_hojas": len(hojas),
            "hojas": [h.get('nombre', 'Hoja') for h in hojas],
            "excel_base64": excel_base64,
            "nombre_archivo": "Reporte_Completo.xlsx"
        }
        
        return Response(respuesta, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error exportando Excel múltiple: {str(e)}")
        return Response(
            {'error': f'Error al generar Excel: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
