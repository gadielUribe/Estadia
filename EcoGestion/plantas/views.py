from django.shortcuts import render, redirect, get_object_or_404
from .forms import plantaForm
from .models import plantaArbol

# Pagina de Incio para CRUD de plantas y árboles
def inicio(request):
    plantas = plantaArbol.objects.all().order_by('id_planta')
    return render(request, 'arboles/read.html', {'plantas': plantas})

# Crear un nuevo árbol o planta
def crear(request):
    if request.method == 'POST': 
        form = plantaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear')
    else:
        form = plantaForm()

    return render(request, 'arboles/create.html', {'form': form})

# Editar un árbol o planta existente
def editar(request, id_arbol):
    arbol = get_object_or_404(plantaArbol, pk=id_arbol)
    if request.method == 'POST':
        form = plantaForm(request.POST, instance=arbol)
        if form.is_valid():
            form.save() 
            return redirect('inicio')
    else:
        form = plantaForm(instance=arbol)
    return render(request, 'arboles/update.html', {'form':form, 'arbol':arbol})

# Eliminar un árbol o planta existente
def eliminar(request, id_arbol):
    arbol = get_object_or_404(plantaArbol, pk=id_arbol)
    if request.method == 'POST':
        arbol.delete()
        return redirect('inicio')
        
    return render(request, 'arboles/delete.html', {'arbol':arbol})
    