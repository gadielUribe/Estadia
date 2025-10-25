from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import incidenciaForm
from .models import incidenciaAmbiental

def es_privilegio(user):
    return user.is_authenticated and getattr(user, "rol", None) in ["administrador"]

# Pagina de Incio para incidencias ambientales
@login_required
def inicio(request):
    incidencia = incidenciaAmbiental.objects.all().order_by('id_incidencia')
    
    return render(request, 'incidencias/read.html', {'incidencia': incidencia})

# Crear una nueva incidencia ambiental
@login_required
@user_passes_test(es_privilegio)
def crear(request):
    if request.method == 'POST': 
        form = incidenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('incidencia_inicio')
    else:
        form = incidenciaForm()

    return render(request, 'incidencias/create.html', {'form': form})

# Editar una incidencia ambiental existente
@login_required
@user_passes_test(es_privilegio)
def editar(request, id_incidencia):
    incidencia = get_object_or_404(incidenciaAmbiental, pk=id_incidencia)
    if request.method == 'POST':
        form = incidenciaForm(request.POST, instance=incidencia)
        if form.is_valid():
            form.save() 
            return redirect('incidencia_inicio')
    else:
        form = incidenciaForm(instance=incidencia)
    return render(request, 'incidencias/update.html', {'form':form, 'incidencia':incidencia})

# Eliminar un árbol o planta existente
@login_required
@user_passes_test(es_privilegio)
def eliminar(request, id_incidencia):
    incidencia = get_object_or_404(incidenciaAmbiental, pk=id_incidencia)
    if request.method == 'POST':
        incidencia.delete()
        return redirect('incidencia_inicio')
        
    return render(request, 'incidencias/delete.html', {'incidencia':incidencia})
