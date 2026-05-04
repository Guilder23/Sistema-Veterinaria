from django.urls import path
from . import views

urlpatterns = [
    path('mascota/<int:mascota_pk>/', views.ver_historial, name='ver_historial'),
    path('nueva-consulta/<int:historial_pk>/', views.nueva_consulta, name='nueva_consulta'),
    path('nuevo-procedimiento/<int:historial_pk>/', views.nuevo_procedimiento, name='nuevo_procedimiento'),
]
