from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_facturas, name='listar_facturas'),
    path('crear/', views.crear_factura, name='crear_factura'),
    path('ver/<int:pk>/', views.ver_factura, name='ver_factura'),
    path('pdf/<int:pk>/', views.generar_factura_pdf, name='factura_pdf'),
    path('historial/', views.historial_pagos, name='historial_pagos'),
    path('pagar/<int:pk>/', views.pagar_factura, name='pagar_factura'),
]
