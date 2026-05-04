from django.db import models

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=5)
    es_medicamento = models.BooleanField(default=False)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

    @property
    def bajo_stock(self):
        return self.stock <= self.stock_minimo
