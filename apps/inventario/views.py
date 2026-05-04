from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto, CategoriaProducto
from django.contrib import messages

@login_required
def listar_productos(request):
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'inventario/listar.html', {'productos': productos})

@login_required
def crear_producto(request):
    categorias = CategoriaProducto.objects.all()
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        nombre = request.POST.get('nombre')
        desc = request.POST.get('descripcion')
        p_compra = request.POST.get('precio_compra')
        p_venta = request.POST.get('precio_venta')
        stock = request.POST.get('stock')
        stock_min = request.POST.get('stock_minimo')
        es_med = request.POST.get('es_medicamento') == 'on'
        vencimiento = request.POST.get('fecha_vencimiento')
        
        try:
            categoria = CategoriaProducto.objects.get(id=categoria_id)
            Producto.objects.create(
                categoria=categoria,
                nombre=nombre,
                descripcion=desc,
                precio_compra=p_compra,
                precio_venta=p_venta,
                stock=stock,
                stock_minimo=stock_min,
                es_medicamento=es_med,
                fecha_vencimiento=vencimiento if vencimiento else None
            )
            messages.success(request, 'Producto agregado al inventario.')
            return redirect('listar_productos')
        except Exception as e:
            messages.error(request, f'Error al agregar producto: {e}')
            
    return render(request, 'inventario/crear.html', {'categorias': categorias})
