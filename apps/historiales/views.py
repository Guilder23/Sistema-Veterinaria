from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import HistorialClinico, Consulta, Procedimiento
from apps.mascotas.models import Mascota
from django.contrib import messages

@login_required
def ver_historial(request, mascota_pk):
    mascota = get_object_or_404(Mascota, pk=mascota_pk)
    # Get or create historial
    historial, created = HistorialClinico.objects.get_or_create(mascota=mascota)
    consultas = historial.consultas.all().order_by('-fecha')
    procedimientos = historial.procedimientos.all().order_by('-fecha')
    
    return render(request, 'historiales/ver.html', {
        'mascota': mascota,
        'historial': historial,
        'consultas': consultas,
        'procedimientos': procedimientos
    })

@login_required
def nueva_consulta(request, historial_pk):
    historial = get_object_or_404(HistorialClinico, pk=historial_pk)
    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        diagnostico = request.POST.get('diagnostico')
        tratamiento = request.POST.get('tratamiento')
        receta = request.POST.get('receta')
        peso = request.POST.get('peso')
        
        try:
            Consulta.objects.create(
                historial=historial,
                veterinario=request.user,
                motivo=motivo,
                diagnostico=diagnostico,
                tratamiento=tratamiento,
                receta=receta,
                peso_actual=peso
            )
            # Update pet weight
            historial.mascota.peso = peso
            historial.mascota.save()
            
            messages.success(request, 'Consulta registrada correctamente.')
            return redirect('ver_historial', mascota_pk=historial.mascota.pk)
        except Exception as e:
            messages.error(request, f'Error al registrar consulta: {e}')
            
    return render(request, 'historiales/nueva_consulta.html', {'historial': historial})

@login_required
def nuevo_procedimiento(request, historial_pk):
    historial = get_object_or_404(HistorialClinico, pk=historial_pk)
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')
        observaciones = request.POST.get('observaciones')
        
        try:
            Procedimiento.objects.create(
                historial=historial,
                tipo=tipo,
                descripcion=descripcion,
                fecha=fecha,
                observaciones=observaciones
            )
            messages.success(request, 'Procedimiento registrado correctamente.')
            return redirect('ver_historial', mascota_pk=historial.mascota.pk)
        except Exception as e:
            messages.error(request, f'Error al registrar procedimiento: {e}')
            
    return render(request, 'historiales/nuevo_procedimiento.html', {'historial': historial})
