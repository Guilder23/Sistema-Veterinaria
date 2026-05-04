from django.urls import path
from . import views

urlpatterns = [
    path('mascota/<int:mascota_pk>/', views.ver_vacunas, name='ver_vacunas'),
    path('registrar-vacuna/<int:mascota_pk>/', views.registrar_vacuna, name='registrar_vacuna'),
    path('registrar-desparasitacion/<int:mascota_pk>/', views.registrar_desparasitacion, name='registrar_desparasitacion'),
]
