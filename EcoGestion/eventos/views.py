from __future__ import annotations

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import EventoForm
from .models import EventoAmbiental


# _rol(user): obtiene el rol del usuario autenticado.
# Entrada: user (objeto User). Salida: cadena con el rol o 'mantenimiento'.
def _rol(user):
    return getattr(user, "rol", "mantenimiento")


# _is_admin(user): verifica si el usuario es administrador o gestor.
# Entrada: user. Salida: True si tiene permisos de administrador/gestor.
def _is_admin(user):
    return _rol(user) in {"administrador", "gestor"}


# _can_manage(user): alias para validar permisos de gestión de eventos.
# Entrada: user. Salida: True si puede crear/editar eventos.
def _can_manage(user):
    return _rol(user) in {"administrador", "gestor"}


@login_required
# evento_list(request): lista eventos con filtros por texto, fechas y organizador.
# Entrada: request (HttpRequest). Salida: HttpResponse con la plantilla de lista.
def evento_list(request):
    qs = EventoAmbiental.objects.select_related("organizador")
    q = (request.GET.get("q") or "").strip()
    fecha_desde = request.GET.get("desde")
    fecha_hasta = request.GET.get("hasta")
    organizador = request.GET.get("organizador")

    if q:
        qs = qs.filter(Q(titulo__icontains=q) | Q(descripcion__icontains=q))
    if organizador:
        qs = qs.filter(organizador_id=organizador)
    if fecha_desde:
        try:
            qs = qs.filter(fecha_inicio__date__gte=fecha_desde)
        except ValueError:
            pass
    if fecha_hasta:
        try:
            qs = qs.filter(fecha_inicio__date__lte=fecha_hasta)
        except ValueError:
            pass

    qs = qs.order_by("-fecha_inicio")

    return render(
        request,
        "eventos/lista.html",
        {
            "eventos": qs,
            "q": q,
            "desde": fecha_desde,
            "hasta": fecha_hasta,
            "organizador": organizador,
        },
    )


@login_required
@user_passes_test(_can_manage)
# evento_create(request): crea un evento ambiental.
# Entrada: request (HttpRequest). Salida: redirección a lista o formulario con errores.
def evento_create(request):
    if request.method == "POST":
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("eventos:lista")
    else:
        form = EventoForm(initial={"organizador": request.user.pk})
    return render(request, "eventos/form.html", {"form": form, "accion": "Nuevo"})


@login_required
@user_passes_test(_can_manage)
# evento_update(request, pk): edita un evento existente.
# Entrada: request (HttpRequest), pk (id del evento). Salida: redirección o recarga de formulario.
def evento_update(request, pk: int):
    evento = get_object_or_404(EventoAmbiental, pk=pk)
    if request.method == "POST":
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect("eventos:lista")
    else:
        form = EventoForm(instance=evento)
    return render(request, "eventos/form.html", {"form": form, "accion": "Editar"})


@login_required
@user_passes_test(_can_manage)
# evento_delete(request, pk): elimina un evento seleccionado.
# Entrada: request (HttpRequest), pk (id del evento). Salida: redirección tras eliminar.
def evento_delete(request, pk: int):
    evento = get_object_or_404(EventoAmbiental, pk=pk)
    if request.method == "POST":
        evento.delete()
        return redirect("eventos:lista")
    return render(request, "eventos/confirm_delete.html", {"evento": evento})


@login_required
# eventos_feed(request): entrega eventos en formato JSON para el calendario.
# Entrada: request con parámetros start/end ISO. Salida: JsonResponse con eventos.
def eventos_feed(request):
    start = request.GET.get("start")
    end = request.GET.get("end")
    try:
        start_dt = timezone.datetime.fromisoformat(start) if start else None
        end_dt = timezone.datetime.fromisoformat(end) if end else None
        if start_dt and timezone.is_naive(start_dt):
            start_dt = timezone.make_aware(start_dt)
        if end_dt and timezone.is_naive(end_dt):
            end_dt = timezone.make_aware(end_dt)
    except Exception:
        return HttpResponseBadRequest("Rango inválido")

    qs = EventoAmbiental.objects.all()
    if start_dt:
        qs = qs.filter(fecha_inicio__gte=start_dt)
    if end_dt:
        qs = qs.filter(fecha_inicio__lte=end_dt)

    eventos = []
    for evento in qs:
        eventos.append(
            {
                "id": evento.id,
                "title": evento.titulo,
                "start": evento.fecha_inicio.isoformat(),
                "end": evento.fecha_fin.isoformat() if evento.fecha_fin else None,
                "allDay": False,
                "editable": False,
                "backgroundColor": "#8e44ad",
                "borderColor": "#8e44ad",
                "extendedProps": {
                    "category": "evento",
                    "descripcion": evento.descripcion,
                    "organizador": getattr(evento.organizador, "nombre_completo", None),
                },
            }
        )
    return JsonResponse(eventos, safe=False)
