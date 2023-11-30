from django.urls import path
from .views import buscar

urlpatterns = [
    path('buscar/', buscar, name='buscar'),
    # Otras rutas pueden estar aquí
]

