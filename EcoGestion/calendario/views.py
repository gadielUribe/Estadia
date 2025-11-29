from __future__ import annotations

from datetime import datetime, timedelta, time

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from plantas.models import plantaArbol
from mantenimiento.models import TareaMantenimiento
from eventos.models import EventoAmbiental


def _user_role(user) -> str:
    return getattr(user, "rol", "mantenimiento")


def _horizon_days() -> int:
    return 60


def ensure_future_tasks(horizon_days: int | None = None):
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
def calendario_view(request):
    role = _user_role(request.user)
    context = {
        "user_role": role,
        "can_edit": role in {"administrador", "gestor"},
        "can_mark_done": role in {"administrador", "gestor", "mantenimiento"},
    }
    return render(request, "calendario/calendario.html", context)


@login_required
def tareas_feed(request):
    # Importante: no autogenerar tareas aquí para evitar que reaparezcan
    # después de que el usuario las elimine manualmente desde el CRUD.
    # La generación automática se hace al crear/editar (opcional) o
    # mediante una tarea programada si se desea.

    start_str = request.GET.get("start")
    end_str = request.GET.get("end")
    try:
        start = datetime.fromisoformat(start_str) if start_str else None
        end = datetime.fromisoformat(end_str) if end_str else None
        if start and timezone.is_naive(start):
            start = timezone.make_aware(start)
        if end and timezone.is_naive(end):
            end = timezone.make_aware(end)
    except Exception:
        return HttpResponseBadRequest("Rango de fechas inválido")

    qs = TareaMantenimiento.objects.select_related("planta")
    role = _user_role(request.user)
    if role == "mantenimiento":
        qs = qs.filter(usuario_responsable=request.user)
    if start:
        qs = qs.filter(fecha_programada__gte=start)
    if end:
        qs = qs.filter(fecha_programada__lte=end)

    events = []
    now = timezone.now()
    for t in qs:
        responsable = None
        try:
            responsable = t.usuario_responsable.nombre_completo if t.usuario_responsable else None
        except Exception:
            responsable = None
        events.append(
            {
                "id": t.id,
                "title": f"[{t.tipo}] {t.planta.nombre_comun}",
                "start": t.fecha_programada.isoformat(),
                "allDay": False,
                "editable": role in {"administrador", "gestor"},
                "backgroundColor": _color_for_tipo(t.tipo, t.estado),
                "extendedProps": {
                    "tipo": t.tipo,
                    "estado": t.estado,
                    "planta_id": t.planta.id_planta,
                    "planta_nombre": t.planta.nombre_comun,
                    "vencida": (t.estado == TareaMantenimiento.ESTADO_PENDIENTE and t.fecha_programada < now),
                    "responsable": responsable,
                    "category": "tarea",
                    "puedeEditar": role in {"administrador", "gestor"},
                    "puedeMarcar": role in {"administrador", "gestor", "mantenimiento"},
                },
            }
        )

    return JsonResponse(events, safe=False)


def _color_for_tipo(tipo: str, estado: str) -> str:
    base = {"riego": "#2D9CDB", "poda": "#27AE60", "fumigacion": "#F2994A"}.get(tipo, "#7f8c8d")
    if estado == TareaMantenimiento.ESTADO_REALIZADA:
        return "#95a5a6"
    return base


@login_required
def tarea_marcar_realizada(request, tarea_id: int):
    if request.method != "POST":
        return HttpResponseBadRequest("Método inválido")
    tarea = get_object_or_404(TareaMantenimiento, id=tarea_id)
    role = _user_role(request.user)
    if role not in {"administrador", "gestor", "mantenimiento"}:
        return HttpResponseForbidden("Sin permisos")
    obs = request.POST.get("observaciones") or None
    tarea.marcar_realizada(by_user=request.user, observaciones=obs)
    return JsonResponse({"ok": True, "estado": tarea.estado})


@login_required
def tarea_actualizar(request, tarea_id: int):
    if request.method != "POST":
        return HttpResponseBadRequest("Método inválido")
    tarea = get_object_or_404(TareaMantenimiento, id=tarea_id)
    role = _user_role(request.user)
    if role not in {"administrador", "gestor"}:
        return HttpResponseForbidden("Sin permisos para editar")
    nueva_fecha = request.POST.get("fecha_programada")
    nuevo_tipo = request.POST.get("tipo")
    obs = request.POST.get("observaciones")
    changed = False
    if nueva_fecha:
        try:
            dt = datetime.fromisoformat(nueva_fecha)
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt)
            tarea.fecha_programada = dt
            changed = True
        except Exception:
            return HttpResponseBadRequest("Fecha inválida")
    if nuevo_tipo in {t[0] for t in TareaMantenimiento.TIPOS}:
        tarea.tipo = nuevo_tipo
        changed = True
    if obs is not None:
        tarea.observaciones = obs
        changed = True
    if changed:
        tarea.save()
    return JsonResponse({"ok": True})
