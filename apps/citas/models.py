from django.db import models
from apps.mascotas.models import Mascota
from django.conf import settings

class Cita(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('atendida', 'Atendida'),
        ('cancelada', 'Cancelada'),
    )
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas')
    veterinario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    notas = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.mascota.nombre}"

    class Meta:
        ordering = ['fecha', 'hora']
