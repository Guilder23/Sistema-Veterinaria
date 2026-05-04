from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.facturacion.models import Factura
from apps.mascotas.models import Mascota
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
import json

@login_required
def reportes_general(request):
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    
    # 1. Financial Stats
    facturas_mes = Factura.objects.filter(fecha__gte=start_of_month, pagado=True)
    total_revenue = facturas_mes.aggregate(Sum('total'))['total__sum'] or 0
    avg_ticket = facturas_mes.aggregate(Avg('total'))['total__avg'] or 0
    
    # 2. Revenue Chart (Last 30 days)
    last_30_days = today - timezone.timedelta(days=30)
    daily_revenue = Factura.objects.filter(fecha__gte=last_30_days, pagado=True) \
        .annotate(day=TruncDay('fecha')) \
        .values('day') \
        .annotate(total=Sum('total')) \
        .order_by('day')
    
    daily_labels = [data['day'].strftime('%d %b') for data in daily_revenue]
    daily_values = [float(data['total']) for data in daily_revenue]
    
    # 3. Species Distribution
    especies_data = Mascota.objects.values('especie').annotate(count=Count('id')).order_by('-count')
    especies_labels = [data['especie'] for data in especies_data]
    especies_values = [data['count'] for data in especies_data]
    
    # 4. Top Products (Most sold)
    from apps.facturacion.models import DetalleFactura
    top_products = DetalleFactura.objects.values('producto__nombre') \
        .annotate(total_qty=Sum('cantidad')) \
        .order_by('-total_qty')[:5]
    
    prod_labels = [p['producto__nombre'] for p in top_products]
    prod_values = [p['total_qty'] for p in top_products]
    
    context = {
        'total_revenue': total_revenue,
        'avg_ticket': round(avg_ticket, 2),
        'total_pets': Mascota.objects.count(),
        'daily_labels': json.dumps(daily_labels),
        'daily_values': json.dumps(daily_values),
        'especies_labels': json.dumps(especies_labels),
        'especies_values': json.dumps(especies_values),
        'prod_labels': json.dumps(prod_labels),
        'prod_values': json.dumps(prod_values),
    }
    return render(request, 'reportes/general.html', context)
