from django.urls import path
from . import views

urlpatterns = [
    path('mascota/<int:mascota_pk>/', views.ver_historial, name='ver_historial'),
    path('nueva-consulta/<int:historial_pk>/', views.nueva_consulta, name='nueva_consulta'),
]
