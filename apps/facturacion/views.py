from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Factura, DetalleFactura
from apps.clientes.models import Cliente
from apps.inventario.models import Producto
from django.contrib import messages
from django.db import transaction

@login_required
def listar_facturas(request):
    tipo = request.GET.get('tipo')
    if tipo:
        facturas = Factura.objects.filter(tipo=tipo).order_by('-fecha')
    else:
        facturas = Factura.objects.all().order_by('-fecha')
    return render(request, 'facturacion/listar.html', {
        'facturas': facturas,
        'tipo_actual': tipo
    })

@login_required
def crear_factura(request):
    clientes = Cliente.objects.all()
    productos = Producto.objects.filter(stock__gt=0)
    
    # Get initial data from GET params
    initial_cliente = request.GET.get('cliente')
    initial_tipo = request.GET.get('tipo', 'venta')
    initial_servicio = request.GET.get('servicio', '')
    
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        metodo_pago = request.POST.get('metodo_pago')
        tipo = request.POST.get('tipo', 'venta')
        
        producto_ids = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')
        # New for services/attention
        servicios = request.POST.getlist('servicios[]')
        precios_servicios = request.POST.getlist('precios_servicios[]')
        
        try:
            with transaction.atomic():
                cliente = Cliente.objects.get(id=cliente_id)
                factura = Factura.objects.create(
                    cliente=cliente,
                    metodo_pago=metodo_pago,
                    tipo=tipo,
                    total=0
                )
                
                total_factura = 0
                
                # Handle products
                for i in range(len(producto_ids)):
                    if not producto_ids[i]: continue
                    prod = Producto.objects.get(id=producto_ids[i])
                    cant = int(cantidades[i])
                    
                    if prod.stock < cant:
                        raise Exception(f"Stock insuficiente para {prod.nombre}")
                        
                    subtotal = prod.precio_venta * cant
                    DetalleFactura.objects.create(
                        factura=factura,
                        producto=prod,
                        cantidad=cant,
                        precio_unitario=prod.precio_venta,
                        subtotal=subtotal
                    )
                    prod.stock -= cant
                    prod.save()
                    total_factura += subtotal
                
                # Handle services (attention)
                for i in range(len(servicios)):
                    if not servicios[i]: continue
                    nombre_servicio = servicios[i]
                    precio = float(precios_servicios[i])
                    
                    DetalleFactura.objects.create(
                        factura=factura,
                        servicio=nombre_servicio,
                        cantidad=1,
                        precio_unitario=precio,
                        subtotal=precio
                    )
                    total_factura += precio
                
                factura.total = total_factura
                factura.save()
                
                messages.success(request, f'Factura #{factura.id} ({factura.get_tipo_display()}) generada correctamente.')
                return redirect('listar_facturas')
        except Exception as e:
            messages.error(request, f'Error al generar factura: {e}')
            
    return render(request, 'facturacion/crear.html', {
        'clientes': clientes,
        'productos': productos,
        'initial_cliente': initial_cliente,
        'initial_tipo': initial_tipo,
        'initial_servicio': initial_servicio
    })

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io

@login_required
def ver_factura(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    return render(request, 'facturacion/ver.html', {'factura': factura})

@login_required
def generar_factura_pdf(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    template = get_template('facturacion/factura_pdf.html')
    context = {
        'factura': factura,
        'empresa': {
            'nombre': 'VetCare',
            'direccion': 'Calle Principal #123, Ciudad',
            'telefono': '+123 456 789',
            'rnc': '123-45678-9'
        }
    }
    html = template.render(context)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error al generar PDF', status=400)

@login_required
def historial_pagos(request):
    facturas = Factura.objects.all().order_by('-fecha')
    return render(request, 'facturacion/historial.html', {'facturas': facturas})

@login_required
def pagar_factura(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    if not factura.pagado:
        factura.pagado = True
        factura.save()
        messages.success(request, f'Pago de la Factura #{factura.id} registrado correctamente.')
    return redirect('listar_facturas')

# Export views if needed for debugging or validation
# print("URLs registered in facturacion: listar_facturas, crear_factura, ver_factura, factura_pdf, historial_pagos, pagar_factura")

