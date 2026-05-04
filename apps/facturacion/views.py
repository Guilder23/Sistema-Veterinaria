from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Factura, DetalleFactura
from apps.clientes.models import Cliente
from apps.inventario.models import Producto
from django.contrib import messages
from django.db import transaction

@login_required
def listar_facturas(request):
    facturas = Factura.objects.all().order_by('-fecha')
    return render(request, 'facturacion/listar.html', {'facturas': facturas})

@login_required
def crear_factura(request):
    clientes = Cliente.objects.all()
    productos = Producto.objects.filter(stock__gt=0)
    
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        metodo_pago = request.POST.get('metodo_pago')
        
        # In a real app, products would be sent as an array/json
        # For simplicity, we'll take a few from the form
        producto_ids = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')
        
        try:
            with transaction.atomic():
                cliente = Cliente.objects.get(id=cliente_id)
                factura = Factura.objects.create(
                    cliente=cliente,
                    metodo_pago=metodo_pago,
                    total=0
                )
                
                total_factura = 0
                for i in range(len(producto_ids)):
                    prod = Producto.objects.get(id=producto_ids[i])
                    cant = int(cantidades[i])
                    subtotal = prod.precio_venta * cant
                    
                    DetalleFactura.objects.create(
                        factura=factura,
                        producto=prod,
                        cantidad=cant,
                        precio_unitario=prod.precio_venta,
                        subtotal=subtotal
                    )
                    
                    # Update stock
                    prod.stock -= cant
                    prod.save()
                    
                    total_factura += subtotal
                
                factura.total = total_factura
                factura.save()
                
                messages.success(request, f'Factura #{factura.id} generada correctamente.')
                return redirect('listar_facturas')
        except Exception as e:
            messages.error(request, f'Error al generar factura: {e}')
            
    return render(request, 'facturacion/crear.html', {
        'clientes': clientes,
        'productos': productos
    })
