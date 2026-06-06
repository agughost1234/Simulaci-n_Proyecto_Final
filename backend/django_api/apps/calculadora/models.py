"""
Modelos para la Calculadora de Métodos Numéricos.
Base de datos para almacenar resultados de cálculos y operaciones.
"""
from django.db import models
from django.utils.timezone import now


class BaseCalculo(models.Model):
    """Modelo base para todos los cálculos con campos comunes."""
    
    ESTADO_CHOICES = [
        ('exito', 'Éxito'),
        ('max_iter_alcanzado', 'Máx. Iteraciones Alcanzado'),
        ('error', 'Error'),
        ('pendiente', 'Pendiente'),
    ]
    
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    descripcion = models.TextField(blank=True, null=True)
    resultado = models.JSONField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['-fecha_creacion']


class Biseccion(BaseCalculo):
    """Método de Bisección para ecuaciones no lineales."""
    
    expresion = models.TextField()
    a_inicial = models.FloatField()
    b_inicial = models.FloatField()
    tolerancia = models.FloatField()
    max_iteraciones = models.IntegerField()
    raiz_aproximada = models.FloatField(null=True, blank=True)
    iteraciones_realizadas = models.IntegerField(null=True, blank=True)
    historial_iteraciones = models.JSONField(default=list, blank=True)
    
    class Meta:
        verbose_name = 'Bisección'
        verbose_name_plural = 'Bisecciones'
        
    def __str__(self):
        return f"Bisección: {self.expresion} en [{self.a_inicial}, {self.b_inicial}]"


class NewtonRaphson(BaseCalculo):
    """Método de Newton-Raphson para ecuaciones no lineales."""
    
    expresion = models.TextField()
    x_inicial = models.FloatField()
    tolerancia = models.FloatField()
    max_iteraciones = models.IntegerField()
    raiz_aproximada = models.FloatField(null=True, blank=True)
    iteraciones_realizadas = models.IntegerField(null=True, blank=True)
    historial_iteraciones = models.JSONField(default=list, blank=True)
    
    class Meta:
        verbose_name = 'Newton-Raphson'
        verbose_name_plural = 'Newton-Raphsons'
        
    def __str__(self):
        return f"Newton-Raphson: {self.expresion} desde x₀={self.x_inicial}"


class CambioDeBase(BaseCalculo):
    """Transformación de números entre diferentes bases numéricas."""
    
    numero_original = models.CharField(max_length=100)
    base_origen = models.IntegerField()
    base_destino = models.IntegerField()
    numero_convertido = models.CharField(max_length=100, null=True, blank=True)
    max_iteraciones = models.IntegerField(default=15)
    historial_pasos = models.JSONField(default=list, blank=True)
    
    class Meta:
        verbose_name = 'Cambio de Base'
        verbose_name_plural = 'Cambios de Base'
        
    def __str__(self):
        return f"Base {self.base_origen} → Base {self.base_destino}: {self.numero_original}"


class CalculoError(BaseCalculo):
    """Cálculo de errores absolutos, relativos y porcentuales."""
    
    valor_verdadero = models.FloatField()
    valor_aproximado = models.FloatField()
    error_absoluto = models.FloatField(null=True, blank=True)
    error_relativo = models.FloatField(null=True, blank=True)
    error_porcentual = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Cálculo de Error'
        verbose_name_plural = 'Cálculos de Error'
        
    def __str__(self):
        return f"Error: Verdadero={self.valor_verdadero}, Aproximado={self.valor_aproximado}"


class Polinomio(BaseCalculo):
    """Operaciones con polinomios y Series de Taylor."""
    
    TIPO_OPERACION = [
        ('taylor', 'Series de Taylor'),
        ('evaluacion', 'Evaluación'),
        ('derivada', 'Derivada'),
        ('integral', 'Integral'),
    ]
    
    expresion = models.TextField()
    tipo_operacion = models.CharField(max_length=20, choices=TIPO_OPERACION)
    centro = models.FloatField(null=True, blank=True, help_text="Centro para Series de Taylor")
    grado = models.IntegerField(null=True, blank=True)
    punto_evaluacion = models.FloatField(null=True, blank=True)
    resultado_polinomio = models.TextField(null=True, blank=True)
    coeficientes = models.JSONField(default=list, blank=True)
    
    class Meta:
        verbose_name = 'Polinomio'
        verbose_name_plural = 'Polinomios'
        
    def __str__(self):
        return f"{self.tipo_operacion.title()}: {self.expresion}"


class InterpolacionLagrange(BaseCalculo):
    """Interpolación de Lagrange para aproximación polinomial."""
    
    puntos_x = models.JSONField(help_text="Lista de valores x")
    puntos_y = models.JSONField(help_text="Lista de valores y correspondientes")
    x_evaluacion = models.FloatField(null=True, blank=True)
    y_aproximado = models.FloatField(null=True, blank=True)
    polinomio_resultado = models.TextField(null=True, blank=True)
    coeficientes = models.JSONField(default=list, blank=True)
    error_interpolacion = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Interpolación de Lagrange'
        verbose_name_plural = 'Interpolaciones de Lagrange'
        
    def __str__(self):
        return f"Lagrange: {len(self.puntos_x)} puntos"


class DiferenciasNivel(BaseCalculo):
    """Diferencias Divididas de Newton para interpolación."""
    
    puntos_x = models.JSONField(help_text="Lista de valores x")
    puntos_y = models.JSONField(help_text="Lista de valores y correspondientes")
    x_evaluacion = models.FloatField(null=True, blank=True)
    y_aproximado = models.FloatField(null=True, blank=True)
    tabla_diferencias = models.JSONField(default=list, blank=True)
    coeficientes = models.JSONField(default=list, blank=True)
    error_interpolacion = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Diferencias Divididas'
        verbose_name_plural = 'Diferencias Divididas'
        
    def __str__(self):
        return f"Diferencias Divididas: {len(self.puntos_x)} puntos"


class AjusteCurvas(BaseCalculo):
    """Ajuste de curvas por mínimos cuadrados."""
    
    TIPO_AJUSTE = [
        ('lineal', 'Lineal: y = ax + b'),
        ('cuadratica', 'Cuadrática: y = ax² + bx + c'),
        ('exponencial', 'Exponencial: y = ae^(bx)'),
        ('potencia', 'Potencia: y = ax^b'),
        ('polinomial', 'Polinomial'),
    ]
    
    puntos_x = models.JSONField(help_text="Lista de valores x")
    puntos_y = models.JSONField(help_text="Lista de valores y")
    tipo_ajuste = models.CharField(max_length=20, choices=TIPO_AJUSTE)
    grado = models.IntegerField(null=True, blank=True, help_text="Grado para polinomios")
    coeficientes = models.JSONField(default=list, blank=True)
    ecuacion_ajuste = models.TextField(null=True, blank=True)
    r_cuadrado = models.FloatField(null=True, blank=True, help_text="Coeficiente de determinación R²")
    error_cuadratico_medio = models.FloatField(null=True, blank=True)
    desviacion_estandar = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Ajuste de Curvas'
        verbose_name_plural = 'Ajustes de Curvas'
        
    def __str__(self):
        return f"Ajuste {self.tipo_ajuste}: {len(self.puntos_x)} puntos"


class CalculoDerivada(BaseCalculo):
    """Cálculo de derivadas numéricas y analíticas."""
    
    METODO_DERIVADA = [
        ('diferencias_finitas', 'Diferencias Finitas'),
        ('diferencias_centrales', 'Diferencias Centrales'),
        ('analitica', 'Analítica'),
    ]
    
    expresion = models.TextField()
    metodo = models.CharField(max_length=25, choices=METODO_DERIVADA)
    punto_evaluacion = models.FloatField()
    h = models.FloatField(null=True, blank=True, help_text="Paso para métodos numéricos")
    derivada_valor = models.FloatField(null=True, blank=True)
    derivada_expresion = models.TextField(null=True, blank=True)
    segunda_derivada = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Cálculo de Derivada'
        verbose_name_plural = 'Cálculos de Derivadas'
        
    def __str__(self):
        return f"Derivada: {self.expresion} en x={self.punto_evaluacion}"


class Reporte(models.Model):
    """Modelo para generar reportes de cálculos."""
    
    TIPO_REPORTE = [
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
        ('json', 'JSON'),
    ]
    
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    tipo_reporte = models.CharField(max_length=10, choices=TIPO_REPORTE)
    contenido = models.BinaryField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)
    
    # Referencias genéricas a los cálculos
    contenido_json = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return f"{self.nombre} ({self.tipo_reporte})"
