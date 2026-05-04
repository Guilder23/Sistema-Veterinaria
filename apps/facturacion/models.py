from django.db import models
from apps.clientes.models import Cliente
from apps.inventario.models import Producto

class Factura(models.Model):
    METODO_PAGO_CHOICES = (
        ('efectivo', 'Efectivo'),
        ('qr', 'QR / Transferencia'),
        ('tarjeta', 'Tarjeta'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='facturas')
    fecha = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pagado = models.BooleanField(default=True)

    def __str__(self):
        return f"Factura #{self.id} - {self.cliente.nombre_completo}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    servicio = models.CharField(max_length=200, blank=True, null=True)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.id} - {self.factura.id}"
