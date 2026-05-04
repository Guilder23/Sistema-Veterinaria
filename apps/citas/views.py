from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cita
from apps.mascotas.models import Mascota
from apps.usuarios.models import Usuario
from django.contrib import messages
from django.utils import timezone

from django.http import JsonResponse
from datetime import datetime, time, timedelta

@login_required
def listar_citas(request):
    citas = Cita.objects.all().order_by('fecha', 'hora')
    return render(request, 'citas/listar.html', {'citas': citas})

@login_required
def calendario_citas(request):
    return render(request, 'citas/calendario.html')

@login_required
def eventos_citas(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    citas = Cita.objects.filter(estado__in=['pendiente', 'confirmada', 'atendida'])
    if start and end:
        citas = citas.filter(fecha__range=[start.split('T')[0], end.split('T')[0]])
        
    eventos = []
    for cita in citas:
        color = '#f6c23e' # pendiente
        if cita.estado == 'confirmada': color = '#4e73df'
        elif cita.estado == 'atendida': color = '#1cc88a'
        
        eventos.append({
            'id': cita.id,
            'title': f"{cita.mascota.nombre} ({cita.motivo})",
            'start': f"{cita.fecha}T{cita.hora}",
            'color': color,
            'url': f"/citas/", # Redirect to list or detail
        })
    return JsonResponse(eventos, safe=False)

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
def obtener_horas_disponibles(request):
    fecha_str = request.GET.get('fecha')
    veterinario_id = request.GET.get('veterinario')
    
    if not fecha_str:
        return JsonResponse({'error': 'Fecha requerida'}, status=400)
    
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Formato de fecha inválido'}, status=400)
    
    # Horario de atención: 08:00 a 18:00 cada 30 min
    horas_posibles = []
    start_time = time(8, 0)
    end_time = time(18, 0)
    current = datetime.combine(fecha, start_time)
    until = datetime.combine(fecha, end_time)
    
    while current < until:
        horas_posibles.append(current.time().strftime('%H:%M'))
        current += timedelta(minutes=30)
    
    # Citas ya ocupadas para ese día y veterinario
    citas_ocupadas = Cita.objects.filter(fecha=fecha, estado__in=['pendiente', 'confirmada', 'atendida'])
    if veterinario_id:
        citas_ocupadas = citas_ocupadas.filter(veterinario_id=veterinario_id)
        
    horas_ocupadas = [c.hora.strftime('%H:%M') for c in citas_ocupadas]
    
    # Filtrar horas disponibles
    horas_disponibles = [h for h in horas_posibles if h not in horas_ocupadas]
    
    return JsonResponse({'horas': horas_disponibles})

@login_required
def cambiar_estado_cita(request, pk, estado):
    cita = get_object_or_404(Cita, pk=pk)
    if estado in dict(Cita.ESTADO_CHOICES):
        cita.estado = estado
        cita.save()
        messages.success(request, f'Estado de cita actualizado a {cita.get_estado_display()}.')
    return redirect('listar_citas')
