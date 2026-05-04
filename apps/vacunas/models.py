from django.db import models
from apps.mascotas.models import Mascota

class Vacuna(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='vacunas')
    nombre_vacuna = models.CharField(max_length=100)
    fecha_aplicacion = models.DateField()
    proxima_dosis = models.DateField(blank=True, null=True)
    lote = models.CharField(max_length=50, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_vacuna} - {self.mascota.nombre}"

class Desparasitacion(models.Model):
    TIPO_CHOICES = (
        ('interna', 'Interna'),
        ('externa', 'Externa'),
    )
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='desparasitaciones')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    producto = models.CharField(max_length=100)
    fecha_aplicacion = models.DateField()
    proxima_fecha = models.DateField(blank=True, null=True)
    peso_actual = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Desparasitación {self.tipo} - {self.mascota.nombre}"
