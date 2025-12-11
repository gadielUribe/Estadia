from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import incidenciaForm
from .models import incidenciaAmbiental

# es_privilegio(user): valida si el usuario es administrador o gestor.
# Entrada: user (objeto User). Salida: True si tiene permisos para gestionar incidencias.
def es_privilegio(user):
    # Administrador y gestor pueden gestionar incidencias completas
    return user.is_authenticated and getattr(user, "rol", None) in ["administrador", "gestor"]

# Pagina de Incio para incidencias ambientales
@login_required
# inicio(request): muestra listado de incidencias ambientales.
# Entrada: request (HttpRequest). Salida: render de la página de lectura.
def inicio(request):
    incidencia = incidenciaAmbiental.objects.all().order_by('id_incidencia')
    
    return render(request, 'incidencias/read.html', {'incidencia': incidencia})

# Crear una nueva incidencia ambiental
@login_required
@user_passes_test(es_privilegio)
# crear(request): registra una nueva incidencia ambiental.
# Entrada: request (HttpRequest). Salida: redirección al inicio o formulario con errores.
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
# editar(request, id_incidencia): actualiza una incidencia ya registrada.
# Entrada: request (HttpRequest), id_incidencia (ID de la incidencia). Salida: redirección o recarga del formulario.
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
# eliminar(request, id_incidencia): elimina la incidencia seleccionada.
# Entrada: request (HttpRequest), id_incidencia (ID a eliminar). Salida: redirección al inicio.
def eliminar(request, id_incidencia):
    incidencia = get_object_or_404(incidenciaAmbiental, pk=id_incidencia)
    if request.method == 'POST':
        incidencia.delete()
        return redirect('incidencia_inicio')
        
    return render(request, 'incidencias/delete.html', {'incidencia':incidencia})
