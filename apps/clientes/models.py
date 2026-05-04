from django.db import models

class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=200)
    identificacion = models.CharField(max_length=20, unique=True, verbose_name="CI / Identificación")
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_completo

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
