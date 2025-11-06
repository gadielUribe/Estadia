from __future__ import annotations

from datetime import datetime, timedelta, time

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect

from plantas.models import plantaArbol
from .models import TareaMantenimiento
from .forms import TareaForm


def _user_role(user) -> str:
    # Custom user model has `rol`: 'administrador', 'gestor', 'mantenimiento'
    return getattr(user, "rol", "mantenimiento")


def _horizon_days() -> int:
    return 60


def ensure_future_tasks(horizon_days: int | None = None):
    """Genera tareas futuras en una sola tabla según periodicidad por tipo."""
    horizon_days = horizon_days or _horizon_days()
    now = timezone.now()
    horizon_dt = now + timedelta(days=horizon_days)
    inicio_hora = time(9, 0)

    for planta in plantaArbol.objects.all():
        plan = [
            (TareaMantenimiento.TIPO_RIEGO, planta.periodicidad_riego),
            (TareaMantenimiento.TIPO_PODA, planta.periodicidad_poda),
            (TareaMantenimiento.TIPO_FUMIGACION, planta.periodicidad_fumigacion),
        ]
        for tipo, cada_dias in plan:
            try:
                cada = int(cada_dias or 0)
            except Exception:
                cada = 0
            if cada <= 0:
                continue
            last = (
                TareaMantenimiento.objects.filter(planta=planta, tipo=tipo)
                .order_by("-fecha_programada")
                .first()
            )
            if last:
                next_date = last.fecha_programada.date() + timedelta(days=cada)
            else:
                base = planta.fecha_plantacion or now.date()
                next_date = base
            tz = timezone.get_current_timezone()
            while datetime.combine(next_date, inicio_hora, tzinfo=tz) <= horizon_dt:
                run_dt = datetime.combine(next_date, inicio_hora, tzinfo=tz)
                exists = TareaMantenimiento.objects.filter(planta=planta, tipo=tipo, fecha_programada=run_dt).exists()
                if not exists:
                    TareaMantenimiento.objects.create(
                        planta=planta,
                        tipo=tipo,
                        fecha_programada=run_dt,
                        estado=TareaMantenimiento.ESTADO_PENDIENTE,
                    )
                next_date = next_date + timedelta(days=cada)


@login_required
def inicio(request):
    role = _user_role(request.user)
    return render(request, "mantenimiento/inicio.html", {"role": role})


# ------- CRUD sencillo por tipo ---------

@login_required
def tareas_list_tipo(request, tipo: str):
    if tipo not in {t[0] for t in TareaMantenimiento.TIPOS}:
        return HttpResponseBadRequest("Tipo inválido")
    qs = TareaMantenimiento.objects.select_related("planta", "usuario_responsable").filter(tipo=tipo)
    role = _user_role(request.user)
    if role == "mantenimiento":
        qs = qs.filter(usuario_responsable=request.user)
    return render(request, "mantenimiento/tareas_list.html", {"tareas": qs, "tipo": tipo})


@login_required
def tarea_create_tipo(request, tipo: str):
    if tipo not in {t[0] for t in TareaMantenimiento.TIPOS}:
        return HttpResponseBadRequest("Tipo inválido")
    role = _user_role(request.user)
    if role not in {"administrador", "gestor"}:
        return HttpResponseForbidden("Sin permisos")

    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.tipo = tipo
            tarea.save()

            # autogeneración según periodicidad, si aplica
            if form.cleaned_data.get("generar_automaticas"):
                horizonte = form.cleaned_data.get("horizonte_dias") or _horizon_days()
                _generar_siguientes(tarea, horizonte)
            messages.success(request, "Tarea creada")
            return redirect(reverse("mantenimiento:tareas_list_tipo", args=[tipo]))
    else:
        form = TareaForm(initial={"tipo": tipo})
    return render(request, "mantenimiento/tarea_form.html", {"form": form, "tipo": tipo, "accion": "Crear"})


@login_required
def tarea_update(request, pk: int):
    # Para editar desde listado: detectamos tipo por parámetro GET
    tarea = get_object_or_404(TareaMantenimiento, pk=pk)
    role = _user_role(request.user)
    if role not in {"administrador", "gestor"}:
        return HttpResponseForbidden("Sin permisos")

    if request.method == "POST":
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            tarea = form.save()
            # opcionalmente generar siguientes desde nueva fecha
            if form.cleaned_data.get("generar_automaticas"):
                horizonte = form.cleaned_data.get("horizonte_dias") or _horizon_days()
                _generar_siguientes(tarea, horizonte)
            messages.success(request, "Tarea actualizada")
            return redirect(reverse("mantenimiento:tareas_list_tipo", args=[tarea.tipo]))
    else:
        form = TareaForm(instance=tarea)
    return render(request, "mantenimiento/tarea_form.html", {"form": form, "tipo": tarea.tipo, "accion": "Editar"})


@login_required
def tarea_delete(request, pk: int):
    tarea = get_object_or_404(TareaMantenimiento, **{"id": pk})
    role = _user_role(request.user)
    if role not in {"administrador", "gestor"}:
        return HttpResponseForbidden("Sin permisos")
    if request.method == "POST":
        tipo_val = tarea.tipo
        tarea.delete()
        messages.success(request, "Tarea eliminada")
        return redirect(reverse("mantenimiento:tareas_list_tipo", args=[tipo_val]))
    return render(request, "mantenimiento/tarea_confirm_delete.html", {"tarea": tarea})


def _generar_siguientes(tarea: TareaMantenimiento, horizonte_dias: int):
    per_map = {
        TareaMantenimiento.TIPO_RIEGO: tarea.planta.periodicidad_riego,
        TareaMantenimiento.TIPO_PODA: tarea.planta.periodicidad_poda,
        TareaMantenimiento.TIPO_FUMIGACION: tarea.planta.periodicidad_fumigacion,
    }
    cada = int(per_map.get(tarea.tipo) or 0)
    if cada <= 0:
        return
    start = tarea.fecha_programada
    horizon = start + timedelta(days=horizonte_dias)
    cur = start + timedelta(days=cada)
    while cur <= horizon:
        TareaMantenimiento.objects.get_or_create(
            planta=tarea.planta,
            tipo=tarea.tipo,
            fecha_programada=cur,
            defaults={
                "usuario_responsable": tarea.usuario_responsable,
                "herramienta": getattr(tarea, "herramienta", None),
                "producto": getattr(tarea, "producto", None),
                "observaciones": tarea.observaciones,
            },
        )
        cur = cur + timedelta(days=cada)
