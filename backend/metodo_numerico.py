from evaluador import Evaluador
import pandas as pd
import io
import base64
import pandas as pd


class MetodoNumerico:
    def __init__(self, evaluador: Evaluador, tolerancia: float, max_iter: int):
        self.evaluador = evaluador
        self.tol = tolerancia 
        self.max_iter = max_iter 
        self.historial = []  

    def limpiar_historial(self):
        self.historial = []
    
    def generar_excel(self, nombre_archivo):
        if not self.historial:
            print("No hay datos en el historial para generar el Excel.")
            return
        df = pd.DataFrame(self.historial)
        df = df.round(6)  # Redondear a 6 decimales para mejor presentación
        ruta = f"{nombre_archivo}.xlsx"
        df.to_excel(ruta, index=False, engine='openpyxl')
        print(f"Archivo '{ruta}' generado exitosamente.")

    def obtener_excel_base64(self):
        """Genera el Excel en la memoria RAM y lo devuelve como string Base64 para el backend."""
        if not self.historial:
            return None
            
        df = pd.DataFrame(self.historial)
        df = df.round(6)
        
        # Crear un archivo virtual en la memoria RAM
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)
        
        # Convertir el archivo a texto Base64
        excel_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        return excel_base64



        
