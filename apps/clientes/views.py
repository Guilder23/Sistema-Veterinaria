from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cliente
from django.contrib import messages

@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all().order_by('-fecha_registro')
    return render(request, 'clientes/listar.html', {'clientes': clientes})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        identificacion = request.POST.get('identificacion')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        direccion = request.POST.get('direccion')
        
        try:
            Cliente.objects.create(
                nombre_completo=nombre,
                identificacion=identificacion,
                telefono=telefono,
                correo=correo,
                direccion=direccion
            )
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('listar_clientes')
        except Exception as e:
            messages.error(request, f'Error al crear cliente: {e}')
            
    return render(request, 'clientes/crear.html')

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.nombre_completo = request.POST.get('nombre')
        cliente.identificacion = request.POST.get('identificacion')
        cliente.telefono = request.POST.get('telefono')
        cliente.correo = request.POST.get('correo')
        cliente.direccion = request.POST.get('direccion')
        
        try:
            cliente.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('listar_clientes')
        except Exception as e:
            messages.error(request, f'Error al actualizar cliente: {e}')
            
    return render(request, 'clientes/editar.html', {'cliente': cliente})

@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('listar_clientes')
    return render(request, 'clientes/eliminar.html', {'cliente': cliente})
