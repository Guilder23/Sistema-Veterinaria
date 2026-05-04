from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_productos, name='listar_productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
]
