from django.urls import path
from . import views

urlpatterns = [
    path('', views.reportes_general, name='reportes_general'),
]
