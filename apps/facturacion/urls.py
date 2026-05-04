from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_facturas, name='listar_facturas'),
    path('crear/', views.crear_factura, name='crear_factura'),
]
