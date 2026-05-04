from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('clientes/', include('apps.clientes.urls')),
    path('mascotas/', include('apps.mascotas.urls')),
    path('historiales/', include('apps.historiales.urls')),
    path('vacunas/', include('apps.vacunas.urls')),
    path('citas/', include('apps.citas.urls')),
    path('inventario/', include('apps.inventario.urls')),
    path('facturacion/', include('apps.facturacion.urls')),
    path('reportes/', include('apps.reportes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
