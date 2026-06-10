"""
URL configuration for calculadora_numerica project.
Endpoints personalizados para cálculos numéricos.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from apps.calculadora.views import (
    api_root,
    biseccion_calcular,
    newton_raphson_calcular,
    cambios_base_calcular,
    calculo_error,
    calculo_derivada,
)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # API Root
    path('api/', api_root, name='api-root'),
    
    # Cálculos Numéricos - Endpoints personalizados
    path('api/calculos/biseccion/', biseccion_calcular, name='biseccion'),
    path('api/calculos/newton-raphson/', newton_raphson_calcular, name='newton-raphson'),
    path('api/calculos/cambios-base/', cambios_base_calcular, name='cambios-base'),
    path('api/calculos/error/', calculo_error, name='error'),
    path('api/calculos/derivada/', calculo_derivada, name='derivada'),
    
    # OpenAPI Schema & Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
