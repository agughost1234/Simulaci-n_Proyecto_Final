from evaluador import Evaluador

class MetodoNumerico:
    def __init__(self, evaluador: Evaluador, tolerancia: float, max_iter: int):
        self.evaluador = evaluador
        self.tol = tolerancia 
        self.max_iter = max_iter 
        self.historial = []  

    def limpiar_historial(self):
        self.historial = []



        
