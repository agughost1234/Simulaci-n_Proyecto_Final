"""
Configuración de administrador para la Calculadora de Métodos Numéricos.
"""
from django.contrib import admin
from .models import (
    Biseccion, NewtonRaphson, CambioDeBase, CalculoError, Polinomio,
    InterpolacionLagrange, DiferenciasNivel, AjusteCurvas, CalculoDerivada, Reporte
)


@admin.register(Biseccion)
class BiseccionAdmin(admin.ModelAdmin):
    list_display = ('id', 'expresion', 'a_inicial', 'b_inicial', 'raiz_aproximada', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('expresion',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'raiz_aproximada')
    fieldsets = (
        ('Parámetros', {
            'fields': ('expresion', 'a_inicial', 'b_inicial', 'tolerancia', 'max_iteraciones')
        }),
        ('Resultados', {
            'fields': ('raiz_aproximada', 'iteraciones_realizadas', 'historial_iteraciones'),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('estado', 'descripcion')
        }),
        ('Metadata', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NewtonRaphson)
class NewtonRaphsonAdmin(admin.ModelAdmin):
    list_display = ('id', 'expresion', 'x_inicial', 'raiz_aproximada', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('expresion',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'raiz_aproximada')


@admin.register(CambioDeBase)
class CambioDeBaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_original', 'base_origen', 'base_destino', 'numero_convertido', 'estado')
    list_filter = ('estado', 'base_origen', 'base_destino')
    search_fields = ('numero_original',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'numero_convertido')


@admin.register(CalculoError)
class CalculoErrorAdmin(admin.ModelAdmin):
    list_display = ('id', 'valor_verdadero', 'valor_aproximado', 'error_absoluto', 'error_relativo')
    list_filter = ('fecha_creacion',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')


@admin.register(Polinomio)
class PolinomioAdmin(admin.ModelAdmin):
    list_display = ('id', 'expresion', 'tipo_operacion', 'grado', 'estado')
    list_filter = ('tipo_operacion', 'estado', 'fecha_creacion')
    search_fields = ('expresion',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')


@admin.register(InterpolacionLagrange)
class InterpolacionLagrangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'x_evaluacion', 'y_aproximado', 'error_interpolacion', 'estado')
    list_filter = ('estado', 'fecha_creacion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')


@admin.register(DiferenciasNivel)
class DiferenciasNivelAdmin(admin.ModelAdmin):
    list_display = ('id', 'x_evaluacion', 'y_aproximado', 'error_interpolacion', 'estado')
    list_filter = ('estado', 'fecha_creacion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')


@admin.register(AjusteCurvas)
class AjusteCurvasAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_ajuste', 'grado', 'r_cuadrado', 'estado')
    list_filter = ('tipo_ajuste', 'estado', 'fecha_creacion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')


@admin.register(CalculoDerivada)
class CalculoDerivadaAdmin(admin.ModelAdmin):
    list_display = ('id', 'expresion', 'metodo', 'punto_evaluacion', 'derivada_valor', 'estado')
    list_filter = ('metodo', 'estado', 'fecha_creacion')
    search_fields = ('expresion',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo_reporte', 'fecha_creacion')
    list_filter = ('tipo_reporte', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_creacion',)
