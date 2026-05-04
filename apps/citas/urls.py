from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_citas, name='listar_citas'),
    path('calendario/', views.calendario_citas, name='calendario_citas'),
    path('eventos/', views.eventos_citas, name='eventos_citas'),
    path('crear/', views.crear_cita, name='crear_cita'),
    path('obtener-horas/', views.obtener_horas_disponibles, name='obtener_horas'),
    path('cambiar-estado/<int:pk>/<str:estado>/', views.cambiar_estado_cita, name='cambiar_estado_cita'),
]
