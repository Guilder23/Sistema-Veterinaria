from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cita
from apps.mascotas.models import Mascota
from apps.usuarios.models import Usuario
from django.contrib import messages
from django.utils import timezone

@login_required
def listar_citas(request):
    citas = Cita.objects.all().order_by('fecha', 'hora')
    return render(request, 'citas/listar.html', {'citas': citas})

@login_required
def crear_cita(request):
    mascotas = Mascota.objects.all()
    veterinarios = Usuario.objects.filter(rol='veterinario')
    
    if request.method == 'POST':
        mascota_id = request.POST.get('mascota')
        veterinario_id = request.POST.get('veterinario')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        motivo = request.POST.get('motivo')
        
        try:
            mascota = Mascota.objects.get(id=mascota_id)
            veterinario = Usuario.objects.get(id=veterinario_id) if veterinario_id else None
            
            Cita.objects.create(
                mascota=mascota,
                veterinario=veterinario,
                fecha=fecha,
                hora=hora,
                motivo=motivo
            )
            messages.success(request, 'Cita programada correctamente.')
            return redirect('listar_citas')
        except Exception as e:
            messages.error(request, f'Error al programar cita: {e}')
            
    return render(request, 'citas/crear.html', {
        'mascotas': mascotas,
        'veterinarios': veterinarios
    })

@login_required
def cambiar_estado_cita(request, pk, estado):
    cita = get_object_or_404(Cita, pk=pk)
    if estado in dict(Cita.ESTADO_CHOICES):
        cita.estado = estado
        cita.save()
        messages.success(request, f'Estado de cita actualizado a {cita.get_estado_display()}.')
    return redirect('listar_citas')
