from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('veterinario', 'Veterinario'),
        ('recepcionista', 'Recepcionista'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='admin')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    foto = models.ImageField(upload_to='usuarios/', blank=True, null=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.rol})"
