from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import plantaForm
from .models import plantaArbol
import folium

def es_privilegio(user):
    return user.is_authenticated and getattr(user, "rol", None) in ["administrador", "gestor"]

# Pagina de Incio para CRUD de plantas y árboles
@login_required
def inicio(request):
    plantas = plantaArbol.objects.all().order_by('id_planta')
    m = folium.Map(location=[18.889647,-99.1397134], zoom_start=18) #Ubicacion Mapa

    for p in plantas:
        if (p.lat is not None and p.lng is not None): #Que haya cordenadas
            folium.Marker(
                [float(p.lat), float(p.lng)],
                popup=f"ID: {p.id_planta}" + f" Ubicacion: {p.descripcion_ubicacion}" + f" Procedencia: {p.procedencia}" + f" LLegada: {p.fecha_llegada}",
                #tooltip=getattr(p, "nombre", "Planta")
            ).add_to(m)

    maps = {'map':m._repr_html_()}
    
    return render(request, 'arboles/read.html', {'plantas': plantas, 'maps':maps})

# Crear un nuevo árbol o planta
@login_required
@user_passes_test(es_privilegio)
def crear(request):
    if request.method == 'POST': 
        form = plantaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('crear')
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
    