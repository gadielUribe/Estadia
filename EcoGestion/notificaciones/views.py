from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notificacion


@login_required
def lista_notificaciones(request):
    notis = (
        Notificacion.objects
        .filter(destiny=request.user, eliminar=False)
        .order_by('-timestamp')
    )
    return render(request, 'notificaciones/lista.html', {'notificaciones': notis})