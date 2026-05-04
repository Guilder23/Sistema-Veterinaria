from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.facturacion.models import Factura
from apps.mascotas.models import Mascota
from django.db.models import Sum
from django.utils import timezone

@login_required
def reportes_general(request):
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    
    # Revenue data for chart
    facturas_mes = Factura.objects.filter(fecha__gte=start_of_month, pagado=True)
    total_revenue = facturas_mes.aggregate(Sum('total'))['total__sum'] or 0
    
    # Species count
    perros = Mascota.objects.filter(especie__icontains='perro').count()
    gatos = Mascota.objects.filter(especie__icontains='gato').count()
    otros = Mascota.objects.exclude(especie__icontains='perro').exclude(especie__icontains='gato').count()
    
    context = {
        'total_revenue': total_revenue,
        'perros': perros,
        'gatos': gatos,
        'otros': otros,
    }
    return render(request, 'reportes/general.html', context)
