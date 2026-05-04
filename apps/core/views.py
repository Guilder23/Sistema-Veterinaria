from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.citas.models import Cita
from apps.mascotas.models import Mascota
from apps.clientes.models import Cliente
from apps.facturacion.models import Factura
from django.utils import timezone
from django.db.models import Sum

def landing_page(request):
    return render(request, 'core/index.html')

@login_required
def dashboard(request):
    today = timezone.now().date()
    
    # Stats
    citas_hoy = Cita.objects.filter(fecha=today).count()
    total_mascotas = Mascota.objects.count()
    total_clientes = Cliente.objects.count()
    
    # Total revenue this month
    start_of_month = today.replace(day=1)
    ingresos_mes = Factura.objects.filter(fecha__gte=start_of_month, pagado=True).aggregate(Sum('total'))['total__sum'] or 0
    
    # Recent activity (mix of models)
    # For now, just recent citas
    proximas_citas = Cita.objects.filter(fecha__gte=today).order_by('fecha', 'hora')[:5]
    
    context = {
        'citas_hoy': citas_hoy,
        'total_mascotas': total_mascotas,
        'total_clientes': total_clientes,
        'ingresos_mes': ingresos_mes,
        'proximas_citas': proximas_citas,
    }
    return render(request, 'core/dashboard.html', context)
