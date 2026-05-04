from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def perfil(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.telefono = request.POST.get('telefono')
        
        if request.FILES.get('foto'):
            user.foto = request.FILES.get('foto')
            
        user.save()
        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('perfil')
        
    return render(request, 'usuarios/perfil.html')
