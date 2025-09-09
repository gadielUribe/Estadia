from django.shortcuts import render
from django.http import HttpResponse
from .forms import plantaForm

def inicio(request):
    return HttpResponse("Hola, Mundo. Estás en la aplicación de Plantas.")

def crear(request):
    form = plantaForm()
    return render(request, 'arboles/create.html',
        {
            'form': plantaForm
        })