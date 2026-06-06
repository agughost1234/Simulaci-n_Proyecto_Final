"""
URL configuration for calculadora_numerica project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Import routers from apps
from apps.calculadora.views import (
    BiseccionViewSet, NewtonRaphsonViewSet, CambiosDeBaseViewSet,
    CalculoErrorViewSet, PolinomioViewSet, InterpolacionLagrangeViewSet,
    DiferenciasNivelViewSet, AjusteCurvasViewSet, CalculoDerivadaViewSet
)

# Configure router
router = DefaultRouter()
router.register(r'biseccion', BiseccionViewSet, basename='biseccion')
router.register(r'newton-raphson', NewtonRaphsonViewSet, basename='newton-raphson')
router.register(r'cambios-base', CambiosDeBaseViewSet, basename='cambios-base')
router.register(r'calculo-error', CalculoErrorViewSet, basename='calculo-error')
router.register(r'polinomio', PolinomioViewSet, basename='polinomio')
router.register(r'interpolacion-lagrange', InterpolacionLagrangeViewSet, basename='interpolacion-lagrange')
router.register(r'diferencias-divididas', DiferenciasNivelViewSet, basename='diferencias-divididas')
router.register(r'ajuste-curvas', AjusteCurvasViewSet, basename='ajuste-curvas')
router.register(r'calculo-derivada', CalculoDerivadaViewSet, basename='calculo-derivada')

urlpatterns = [
    path('admin/', admin.site.urls),
    # API v1 endpoints
    path('api/v1/', include(router.urls)),
    # API Documentation (Swagger)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # DRF auth
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
