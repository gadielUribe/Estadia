from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Usuario
from .forms import UsuarioForm

from .forms import LoginForm

def user_login(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            matricula = form.cleaned_data['matricula']
            password = form.cleaned_data['password']
            user = authenticate(request, matricula=matricula, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error = "Matrícula o contraseña incorrectos."
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form, 'error': error})

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def es_administrador(user):
    return user.is_authenticated and user.rol == 'administrador'
@user_passes_test(es_administrador)
def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'registration/usuario_list.html', {'usuarios': usuarios})

@user_passes_test(es_administrador)
def usuario_create(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuario_list')
    else:
        form = UsuarioForm()
    return render(request, 'registration/usuario_form.html', {'form': form})

@user_passes_test(es_administrador)
def usuario_update(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuario_list')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'registration/usuario_form.html', {'form': form})

@user_passes_test(es_administrador)
def usuario_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuario_list')
    return render(request, 'registration/usuario_confirm_delete.html', {'usuario': usuario})