from __future__ import annotations

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import EventoForm
from .models import EventoAmbiental


def _rol(user):
    return getattr(user, "rol", "mantenimiento")


def _is_admin(user):
    return _rol(user) == "administrador"


def _can_manage(user):
    return _rol(user) in {"administrador", "gestor"}


@login_required
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
@user_passes_test(_is_admin)
def evento_delete(request, pk: int):
    evento = get_object_or_404(EventoAmbiental, pk=pk)
    if request.method == "POST":
        evento.delete()
        return redirect("eventos:lista")
    return render(request, "eventos/confirm_delete.html", {"evento": evento})


@login_required
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
