from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.citas.models import Cita
from apps.mascotas.models import Mascota
from apps.clientes.models import Cliente
from apps.facturacion.models import Factura
from apps.inventario.models import Producto
from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
import json

def landing_page(request):
    return render(request, 'core/index.html')

@login_required
def buscar(request):
    query = request.GET.get('q', '')
    if query:
        # Search in pets, clients, and products
        mascotas = Mascota.objects.filter(nombre__icontains=query)
        clientes = Cliente.objects.filter(nombre_completo__icontains=query)
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        mascotas = clientes = productos = []
        
    return render(request, 'core/buscar.html', {
        'mascotas': mascotas,
        'clientes': clientes,
        'productos': productos,
        'query': query
    })

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
    
    # Recent activity
    proximas_citas = Cita.objects.filter(fecha__gte=today).order_by('fecha', 'hora')[:5]
    ultimas_mascotas = Mascota.objects.all().order_by('-fecha_registro')[:5]
    
    # Chart data: Revenue last 6 months
    six_months_ago = today - timezone.timedelta(days=180)
    revenue_data = Factura.objects.filter(fecha__gte=six_months_ago, pagado=True) \
        .annotate(month=TruncMonth('fecha')) \
        .values('month') \
        .annotate(total=Sum('total')) \
        .order_by('month')
    
    chart_labels = [data['month'].strftime('%b') for data in revenue_data]
    chart_values = [float(data['total']) for data in revenue_data]
    
    # Species distribution for pie chart
    especies_data = Mascota.objects.values('especie').annotate(count=Count('id')).order_by('-count')
    especies_labels = [data['especie'] for data in especies_data]
    especies_values = [data['count'] for data in especies_data]
    
    context = {
        'citas_hoy': citas_hoy,
        'total_mascotas': total_mascotas,
        'total_clientes': total_clientes,
        'ingresos_mes': ingresos_mes,
        'proximas_citas': proximas_citas,
        'ultimas_mascotas': ultimas_mascotas,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
        'especies_labels': json.dumps(especies_labels),
        'especies_values': json.dumps(especies_values),
    }
    return render(request, 'core/dashboard.html', context)
