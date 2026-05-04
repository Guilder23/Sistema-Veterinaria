from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_citas, name='listar_citas'),
    path('crear/', views.crear_cita, name='crear_cita'),
    path('estado/<int:pk>/<str:estado>/', views.cambiar_estado_cita, name='cambiar_estado_cita'),
]
