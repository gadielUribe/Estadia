from __future__ import annotations

from datetime import datetime, timedelta, time

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from django.urls import reverse
from django.shortcuts import redirect

from plantas.models import plantaArbol
from voluntarios.models import AsignacionVoluntario
from .models import TareaMantenimiento
from .forms import TareaForm


def _user_role(user) -> str:
    # Custom user model has `rol`: 'administrador', 'gestor', 'mantenimiento'
    return getattr(user, "rol", "mantenimiento")


def _horizon_days() -> int:
    return 60


def _actividad_descripcion(tarea: TareaMantenimiento) -> str:
    return f"{tarea.get_tipo_display()} - {tarea.planta.nombre_comun}"


def _sincronizar_voluntario(tarea: TareaMantenimiento, voluntario, asignado_por):
    queryset = AsignacionVoluntario.objects.filter(tarea_id=tarea.id)
    if voluntario:
        AsignacionVoluntario.objects.update_or_create(
            tarea_id=tarea.id,
            defaults={
                "voluntario": voluntario,
                "actividad": _actividad_descripcion(tarea),
                "evento_id": None,
                "evento_nombre": "",
                "asignado_por": asignado_por,
            },
        )
    else:
        queryset.delete()


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


# ------- CRUD unificado ---------

@login_required
def tareas_list(request):
    qs = TareaMantenimiento.objects.select_related("planta", "usuario_responsable").all()
    role = _user_role(request.user)
    if role == "mantenimiento":
        qs = qs.filter(usuario_responsable=request.user)
    # filtros simples opcionales
    tipo = request.GET.get("tipo")
    if tipo in {t[0] for t in TareaMantenimiento.TIPOS}:
        qs = qs.filter(tipo=tipo)
    tareas = list(qs)
    tarea_ids = [t.id for t in tareas]
    voluntario_map = {}
    if tarea_ids:
        asignaciones = (
            AsignacionVoluntario.objects.select_related("voluntario")
            .filter(tarea_id__in=tarea_ids)
            .order_by("-fecha_asignacion")
        )
        for asign in asignaciones:
            nombre_vol = f"{asign.voluntario.nombre} {asign.voluntario.apellido}".strip()
            voluntario_map.setdefault(asign.tarea_id, nombre_vol)
    for tarea in tareas:
        if tarea.usuario_responsable:
            tarea.responsable_etiqueta = str(tarea.usuario_responsable)
        else:
            tarea.responsable_etiqueta = voluntario_map.get(tarea.id, "-")
    return render(
        request,
        "mantenimiento/tareas_list.html",
        {"tareas": tareas, "tipo": tipo or "todas"},
    )


@login_required
def tarea_create(request):
    role = _user_role(request.user)
    if role not in {"administrador", "gestor"}:
        return HttpResponseForbidden("Sin permisos")

    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            usuario, voluntario = form.get_responsable()
            tarea.usuario_responsable = usuario
            tarea.save()
            _sincronizar_voluntario(tarea, voluntario, request.user)
            if form.cleaned_data.get("repetir") and form.cleaned_data.get("cada_dias") and form.cleaned_data.get("repeticiones"):
                _generar_repetidas(
                    tarea,
                    int(form.cleaned_data["cada_dias"]),
                    int(form.cleaned_data["repeticiones"]),
                    voluntario=voluntario,
                    asignado_por=request.user,
                )
            return redirect(reverse("mantenimiento:tareas_list"))
    else:
        fecha = request.GET.get("fecha")
        initial = {}
        if fecha:
            initial["fecha_programada"] = f"{fecha}T09:00"
        form = TareaForm(initial=initial)
    return render(request, "mantenimiento/tarea_form.html", {"form": form, "tipo": "tarea", "accion": "Crear"})


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
            tarea = form.save(commit=False)
            usuario, voluntario = form.get_responsable()
            tarea.usuario_responsable = usuario
            tarea.save()
            _sincronizar_voluntario(tarea, voluntario, request.user)
            # opcionalmente generar siguientes desde nueva fecha
            if form.cleaned_data.get("repetir") and form.cleaned_data.get("cada_dias") and form.cleaned_data.get("repeticiones"):
                _generar_repetidas(
                    tarea,
                    int(form.cleaned_data["cada_dias"]),
                    int(form.cleaned_data["repeticiones"]),
                    voluntario=voluntario,
                    asignado_por=request.user,
                )
            return redirect(reverse("mantenimiento:tareas_list"))
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
        # Respuesta JSON cuando sea una petición AJAX (fetch desde listado)
        if request.headers.get("x-requested-with") == "XMLHttpRequest" or "application/json" in (request.headers.get("Accept", "")):
            return JsonResponse({"ok": True})
        return redirect(reverse("mantenimiento:tareas_list"))
    return redirect(reverse("mantenimiento:tareas_list"))


def _generar_repetidas(tarea: TareaMantenimiento, cada_dias: int, repeticiones: int, voluntario=None, asignado_por=None):
    start = tarea.fecha_programada
    for i in range(1, repeticiones + 1):
        cur = start + timedelta(days=cada_dias * i)
        nueva_tarea, created = TareaMantenimiento.objects.get_or_create(
            planta=tarea.planta,
            tipo=tarea.tipo,
            fecha_programada=cur,
            defaults={
                "usuario_responsable": tarea.usuario_responsable,
                "herramienta": getattr(tarea, "herramienta", None),
                "producto": getattr(tarea, "producto", None),
                "observaciones": tarea.observaciones,
                "estado": TareaMantenimiento.ESTADO_PENDIENTE,
            },
        )
        if voluntario and created:
            _sincronizar_voluntario(nueva_tarea, voluntario, asignado_por)
