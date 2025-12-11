from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.db import transaction
from datetime import datetime
import folium
from django.db.models import OuterRef, Subquery, CharField, Value
from django.db.models.functions import Coalesce
from salud.models import SaludRegistro
from .forms import plantaForm, PlantaCreateForm
from .models import plantaArbol

# Importa de salud para crear el registro y notificar
from salud.models import SaludRegistro, SaludHistorial
from salud.views import _notificar_si_riesgo  # ya implementado en tu app salud


# es_privilegio(user): valida si el usuario tiene rol administrador o gestor.
# Entrada: user (objeto User). Salida: True si posee privilegios.
def es_privilegio(user):
    return user.is_authenticated and getattr(user, "rol", None) in ["administrador", "gestor"]


# _parse_date(s): convierte un string en fecha con formato YYYY-MM-DD.
# Entrada: s (cadena de fecha). Salida: objeto date o None si falla.
def _parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None

@login_required
# inicio(request): lista las plantas con filtros y muestra el mapa.
# Entrada: request (HttpRequest con filtros opcionales).
# Salida: HttpResponse con listado o partial si la peticion es AJAX.
def inicio(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    qs = plantaArbol.objects.all()

    # --- filtros existentes ---
    q = (request.GET.get("q") or "").strip()
    f_from = request.GET.get("fecha_desde") or ""
    f_to = request.GET.get("fecha_hasta") or ""

    if q:
        qs = qs.filter(
            Q(nombre_comun__icontains=q) |
            Q(nombre_cientifico__icontains=q)
        )

    d_from = _parse_date(f_from)
    d_to = _parse_date(f_to)
    if d_from:
        qs = qs.filter(fecha_plantacion__gte=d_from)
    if d_to:
        qs = qs.filter(fecha_plantacion__lte=d_to)

    # --- ANOTAR el último estado de salud por planta ---
    ultimo_estado = (SaludRegistro.objects
                     .filter(planta_id=OuterRef('pk'))
                     .order_by('-fecha_actualizacion')
                     .values('estado_salud')[:1])

    qs = qs.annotate(
        estado_salud=Coalesce(
            Subquery(ultimo_estado, output_field=CharField()),
            Value('verde')  # valor por defecto si no hay registros
        )
    )

    plantas = qs.order_by('id_planta')

    # --- Mapa con resultados filtrados ---
    m = folium.Map(location=[18.889647, -99.1397134], zoom_start=18)
    for p in plantas:
        if p.lat is not None and p.lng is not None:
            folium.Marker(
                [float(p.lat), float(p.lng)],
                popup=(
                    f"ID: {p.id_planta}<br>"
                    f"Nombre científico: {p.nombre_cientifico}<br>"
                    f"Ubicación: ({p.lat}, {p.lng})"
                )
            ).add_to(m)
    maps = {'map': m._repr_html_()}

    ctx = {
        'plantas': plantas,
        'maps': maps,
        'q': q,
        'fecha_desde': f_from,
        'fecha_hasta': f_to,
        'total': plantas.count(),
    }

    # Si es AJAX, renderiza solo la parte de los resultados.
    if is_ajax:
        return render(request, 'arboles/partials/lista_resultados.html', ctx)

    return render(request, 'arboles/read.html', ctx)


# --- CREAR: usa el form con campos de salud y crea SaludRegistro + Historial + Notificación ---
@login_required
@user_passes_test(es_privilegio)
# crear(request): registra una nueva planta y su estado de salud inicial.
# Entrada: request (HttpRequest). Salida: redireccion al inicio o formulario con errores.
def crear(request):
    if request.method == 'POST':
        form = PlantaCreateForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                planta = form.save()

                estado = form.cleaned_data['estado_salud']
                obs = (form.cleaned_data.get('observaciones') or '').strip()

                # Registro de salud actual
                sr = SaludRegistro.objects.create(
                    planta=planta,
                    estado_salud=estado,
                    usuario=request.user,
                    observaciones=obs
                )

                # Historial
                SaludHistorial.objects.create(
                    planta=planta,
                    usuario=request.user,
                    estado_salud=estado,
                    observaciones=obs
                )

                # Notificar si es amarillo/rojo (si prefieres, usa on_commit)
                # transaction.on_commit(lambda: _notificar_si_riesgo(sr))
                _notificar_si_riesgo(sr)

            return redirect('planta_inicio')
    else:
        form = PlantaCreateForm()

    return render(request, 'arboles/create.html', {'form': form})


# --- EDITAR: se mantiene sin tocar salud (se edita en módulo salud) ---
@login_required
@user_passes_test(es_privilegio)
# editar(request, id_arbol): actualiza la informacion basica de una planta.
# Entrada: request (HttpRequest), id_arbol (identificador de la planta).
# Salida: redireccion al inicio o recarga del formulario.
def editar(request, id_arbol):
    arbol = get_object_or_404(plantaArbol, pk=id_arbol)
    if request.method == 'POST':
        form = plantaForm(request.POST, request.FILES, instance=arbol)
        if form.is_valid():
            form.save()
            return redirect('planta_inicio')
    else:
        form = plantaForm(instance=arbol)
    return render(request, 'arboles/update.html', {'form': form, 'arbol': arbol})


# --- ELIMINAR: sin cambios (usa modal POST) ---
@login_required
@user_passes_test(es_privilegio)
# eliminar(request, id_arbol): elimina una planta seleccionada.
# Entrada: request (HttpRequest), id_arbol (identificador de la planta).
# Salida: redireccion al inicio despues de borrar.
def eliminar(request, id_arbol):
    arbol = get_object_or_404(plantaArbol, pk=id_arbol)
    if request.method == 'POST':
        arbol.delete()
        return redirect('planta_inicio')
    return redirect('planta_inicio')
