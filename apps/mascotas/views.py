from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Mascota
from apps.clientes.models import Cliente
from django.contrib import messages

@login_required
def listar_mascotas(request):
    mascotas = Mascota.objects.all().order_by('-fecha_registro')
    return render(request, 'mascotas/listar.html', {'mascotas': mascotas})

@login_required
def crear_mascota(request):
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        nombre = request.POST.get('nombre')
        especie = request.POST.get('especie')
        raza = request.POST.get('raza')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        peso = request.POST.get('peso')
        sexo = request.POST.get('sexo')
        foto = request.FILES.get('foto')
        
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            Mascota.objects.create(
                cliente=cliente,
                nombre=nombre,
                especie=especie,
                raza=raza,
                fecha_nacimiento=fecha_nacimiento,
                peso=peso,
                sexo=sexo,
                foto=foto
            )
            messages.success(request, 'Mascota registrada correctamente.')
            return redirect('listar_mascotas')
        except Exception as e:
            messages.error(request, f'Error al registrar mascota: {e}')
            
    return render(request, 'mascotas/crear.html', {'clientes': clientes})

@login_required
def editar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        mascota.cliente_id = request.POST.get('cliente')
        mascota.nombre = request.POST.get('nombre')
        mascota.especie = request.POST.get('especie')
        mascota.raza = request.POST.get('raza')
        mascota.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        mascota.peso = request.POST.get('peso')
        mascota.sexo = request.POST.get('sexo')
        if request.FILES.get('foto'):
            mascota.foto = request.FILES.get('foto')
        
        try:
            mascota.save()
            messages.success(request, 'Mascota actualizada correctamente.')
            return redirect('listar_mascotas')
        except Exception as e:
            messages.error(request, f'Error al actualizar mascota: {e}')
            
    return render(request, 'mascotas/editar.html', {'mascota': mascota, 'clientes': clientes})

@login_required
def eliminar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    if request.method == 'POST':
        mascota.delete()
        messages.success(request, 'Mascota eliminada correctamente.')
        return redirect('listar_mascotas')
    return render(request, 'mascotas/eliminar.html', {'mascota': mascota})
