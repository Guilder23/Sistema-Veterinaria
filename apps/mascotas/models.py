from django.db import models
from apps.clientes.models import Cliente

class Mascota(models.Model):
    SEXO_CHOICES = (
        ('M', 'Macho'),
        ('H', 'Hembra'),
    )
    cliente = models.ForeignKey(Cliente, related_name='mascotas', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)  # perro, gato, etc.
    raza = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    foto = models.ImageField(upload_to='mascotas/', blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.especie})"

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"
