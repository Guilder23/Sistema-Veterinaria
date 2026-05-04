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

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    categorias = CategoriaProducto.objects.all()
    if request.method == 'POST':
        producto.categoria_id = request.POST.get('categoria')
        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio_compra = request.POST.get('precio_compra')
        producto.precio_venta = request.POST.get('precio_venta')
        producto.stock = request.POST.get('stock')
        producto.stock_minimo = request.POST.get('stock_minimo')
        producto.es_medicamento = request.POST.get('es_medicamento') == 'on'
        vencimiento = request.POST.get('fecha_vencimiento')
        producto.fecha_vencimiento = vencimiento if vencimiento else None
        
        try:
            producto.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('listar_productos')
        except Exception as e:
            messages.error(request, f'Error al actualizar producto: {e}')
            
    return render(request, 'inventario/editar.html', {'producto': producto, 'categorias': categorias})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado del inventario.')
        return redirect('listar_productos')
    return render(request, 'inventario/eliminar.html', {'producto': producto})

# Gestión de Categorías
@login_required
def listar_categorias(request):
    categorias = CategoriaProducto.objects.all().order_by('nombre')
    return render(request, 'inventario/listar_categorias.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        try:
            CategoriaProducto.objects.create(nombre=nombre, descripcion=descripcion)
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('listar_categorias')
        except Exception as e:
            messages.error(request, f'Error al crear categoría: {e}')
    return render(request, 'inventario/crear_categoria.html')

@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(CategoriaProducto, pk=pk)
    if request.method == 'POST':
        categoria.nombre = request.POST.get('nombre')
        categoria.descripcion = request.POST.get('descripcion')
        try:
            categoria.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('listar_categorias')
        except Exception as e:
            messages.error(request, f'Error al actualizar categoría: {e}')
    return render(request, 'inventario/editar_categoria.html', {'categoria': categoria})

@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(CategoriaProducto, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada correctamente.')
        return redirect('listar_categorias')
    return render(request, 'inventario/eliminar_categoria.html', {'categoria': categoria})
