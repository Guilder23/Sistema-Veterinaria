from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_clientes, name='listar_clientes'),
    path('crear/', views.crear_cliente, name='crear_cliente'),
    path('editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
]
