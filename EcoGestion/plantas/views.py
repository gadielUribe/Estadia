from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from datetime import datetime
from .forms import plantaForm
from .models import plantaArbol
import folium

def es_privilegio(user):
    return user.is_authenticated and getattr(user, "rol", None) in ["administrador", "gestor"]

def _parse_date(s):
    # Espera formato YYYY-MM-DD desde <input type="date">
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None

# Pagina de Incio para CRUD de plantas y árboles (con búsqueda/filtros)
@login_required
def inicio(request):
    qs = plantaArbol.objects.all()

    # --- Filtros ---
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
        # Mantén los valores en el form
        'q': q,
        'fecha_desde': f_from,
        'fecha_hasta': f_to,
        'total': plantas.count(),
    }
    return render(request, 'arboles/read.html', ctx)

# Crear un nuevo árbol o planta
@login_required
@user_passes_test(es_privilegio)
def crear(request):
    if request.method == 'POST': 
        form = plantaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('planta_inicio')
    else:
        form = plantaForm()

    return render(request, 'arboles/create.html', {'form': form})

# Editar un árbol o planta existente
@login_required
@user_passes_test(es_privilegio)
def editar(request, id_arbol):
    arbol = get_object_or_404(plantaArbol, pk=id_arbol)
    if request.method == 'POST':
        form = plantaForm(request.POST, request.FILES, instance=arbol)
        if form.is_valid():
            form.save() 
            return redirect('planta_inicio')
    else:
        form = plantaForm(instance=arbol)
    return render(request, 'arboles/update.html', {'form':form, 'arbol':arbol})

# Eliminar un árbol o planta existente
@login_required
@user_passes_test(es_privilegio)
def eliminar(request, id_arbol):
    arbol = get_object_or_404(plantaArbol, pk=id_arbol)
    if request.method == 'POST':
        arbol.delete()
        return redirect('planta_inicio')
        
    return render(request, 'arboles/delete.html', {'arbol':arbol})
    