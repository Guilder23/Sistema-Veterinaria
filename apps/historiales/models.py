from django.db import models
from apps.mascotas.models import Mascota
from django.conf import settings

class HistorialClinico(models.Model):
    mascota = models.OneToOneField(Mascota, on_delete=models.CASCADE, related_name='historial')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historial de {self.mascota.nombre}"

class Consulta(models.Model):
    historial = models.ForeignKey(HistorialClinico, on_delete=models.CASCADE, related_name='consultas')
    veterinario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    receta = models.TextField(blank=True, null=True)
    peso_actual = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Consulta {self.fecha} - {self.historial.mascota.nombre}"

class Procedimiento(models.Model):
    TIPO_CHOICES = (
        ('cirugia', 'Cirugía'),
        ('limpieza', 'Limpieza Dental'),
        ('otro', 'Otro'),
    )
    historial = models.ForeignKey(HistorialClinico, on_delete=models.CASCADE, related_name='procedimientos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    fecha = models.DateField()
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.fecha}"
