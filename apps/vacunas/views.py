from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vacuna, Desparasitacion
from apps.mascotas.models import Mascota
from django.contrib import messages

@login_required
def ver_vacunas(request, mascota_pk):
    mascota = get_object_or_404(Mascota, pk=mascota_pk)
    vacunas = mascota.vacunas.all().order_by('-fecha_aplicacion')
    desparasitaciones = mascota.desparasitaciones.all().order_by('-fecha_aplicacion')
    
    return render(request, 'vacunas/ver.html', {
        'mascota': mascota,
        'vacunas': vacunas,
        'desparasitaciones': desparasitaciones
    })

@login_required
def registrar_vacuna(request, mascota_pk):
    mascota = get_object_or_404(Mascota, pk=mascota_pk)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        fecha = request.POST.get('fecha')
        proxima = request.POST.get('proxima')
        lote = request.POST.get('lote')
        obs = request.POST.get('observaciones')
        
        try:
            Vacuna.objects.create(
                mascota=mascota,
                nombre_vacuna=nombre,
                fecha_aplicacion=fecha,
                proxima_dosis=proxima if proxima else None,
                lote=lote,
                observaciones=obs
            )
            messages.success(request, 'Vacuna registrada correctamente.')
            return redirect('ver_vacunas', mascota_pk=mascota.pk)
        except Exception as e:
            messages.error(request, f'Error al registrar vacuna: {e}')
            
    return render(request, 'vacunas/registrar_vacuna.html', {'mascota': mascota})

@login_required
def registrar_desparasitacion(request, mascota_pk):
    mascota = get_object_or_404(Mascota, pk=mascota_pk)
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        producto = request.POST.get('producto')
        fecha = request.POST.get('fecha')
        proxima = request.POST.get('proxima')
        peso = request.POST.get('peso')
        
        try:
            Desparasitacion.objects.create(
                mascota=mascota,
                tipo=tipo,
                producto=producto,
                fecha_aplicacion=fecha,
                proxima_fecha=proxima if proxima else None,
                peso_actual=peso
            )
            # Update pet weight
            mascota.peso = peso
            mascota.save()
            
            messages.success(request, 'Desparasitación registrada correctamente.')
            return redirect('ver_vacunas', mascota_pk=mascota.pk)
        except Exception as e:
            messages.error(request, f'Error al registrar desparasitación: {e}')
            
    return render(request, 'vacunas/registrar_desparasitacion.html', {'mascota': mascota})
