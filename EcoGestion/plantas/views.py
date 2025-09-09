from django.shortcuts import render
from django.http import HttpResponse

def inicio(request):
    return HttpResponse("Hola, Mundo. Estás en la aplicación de Plantas.")

def crear(request):
    return render(request, 'arboles/create.html')