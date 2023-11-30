# en tu_proyecto/urls.py

from django.contrib import admin
from django.urls import include, path, re_path
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buscador/', include('buscador.urls')),
    re_path(r'^$', lambda r: HttpResponseRedirect('buscador/buscar')),  # Redirigir la raíz a la búsqueda
]
