from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Notificacion

@login_required
# lista_notificaciones(request): muestra las notificaciones del usuario filtradas por estado.
# Entrada: request (HttpRequest con filtro opcional). Salida: HttpResponse con listado.
def lista_notificaciones(request):
    # filtro: todas | no_leidas | leidas
    f = (request.GET.get("f") or "todas").strip()
    base = Notificacion.objects.filter(destiny=request.user, eliminar=False)

    if f == "no_leidas":
        notis = base.no_leidas()
    elif f == "leidas":
        notis = base.leidas()
    else:
        notis = base

    # contadores para tabs
    total = base.count()
    sin_leer = base.no_leidas().count()
    leidas = base.leidas().count()

    ctx = {
        "notificaciones": notis.order_by('-timestamp'),
        "filtro": f,
        "total": total,
        "sin_leer": sin_leer,
        "leidas": leidas,
    }
    return render(request, 'notificaciones/lista.html', ctx)


# _volver(request, default_name): redirige a la URL previa o a la lista de notificaciones.
# Entrada: request (HttpRequest) y nombre de ruta por defecto. Salida: redirección HTTP.
def _volver(request, default_name='notificaciones:lista'):
    # Intenta volver a la misma vista (mantiene ?f=…)
    return redirect(request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse(default_name))

@login_required
@require_POST
# marcar_leida(request, pk): marca una notificación como leída.
# Entrada: request (HttpRequest), pk (id de la notificación). Salida: redirección de retorno.
def marcar_leida(request, pk):
    n = get_object_or_404(Notificacion, pk=pk, destiny=request.user, eliminar=False)
    if n.no_leido:
        n.no_leido = False
        n.save(update_fields=['no_leido'])
    return _volver(request)

@login_required
@require_POST
@require_POST
# marcar_no_leida(request, pk): marca una notificación como no leída.
# Entrada: request (HttpRequest), pk (id de la notificación). Salida: redirección.
def marcar_no_leida(request, pk):
    n = get_object_or_404(Notificacion, pk=pk, destiny=request.user, eliminar=False)
    if not n.no_leido:
        n.no_leido = True
        n.save(update_fields=['no_leido'])
    return _volver(request)

@login_required
@require_POST
@require_POST
# marcar_todo_leido(request): marca todas las notificaciones como leídas.
# Entrada: request (HttpRequest). Salida: redirección.
def marcar_todo_leido(request):
    Notificacion.objects.filter(destiny=request.user, eliminar=False).marcar_todo_como_leido(destino=request.user)
    return _volver(request)

@login_required
@require_POST
@require_POST
# marcar_todo_no_leido(request): cambia todas las notificaciones a no leídas.
# Entrada: request (HttpRequest). Salida: redirección.
def marcar_todo_no_leido(request):
    Notificacion.objects.filter(destiny=request.user, eliminar=False).marcar_todo_como_no_leido(destino=request.user)
    return _volver(request)
