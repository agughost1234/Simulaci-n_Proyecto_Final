import pandas as pd


class MetodoNumerico:
    def __init__(self, evaluador, tolerancia: float, max_iter: int):
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
        df = df.round(6)
        ruta = f"{nombre_archivo}.xlsx"
        df.to_excel(ruta, index=False, engine='openpyxl')
        print(f"Archivo '{ruta}' generado exitosamente.")
