from django.contrib import admin
from .models import HistorialClinico, Consulta, Procedimiento

admin.site.register(HistorialClinico)
admin.site.register(Consulta)
admin.site.register(Procedimiento)
