from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Usuario
from .forms import LoginForm, UsuarioForm, ValidatedPasswordResetForm

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
                error = "Credenciales inválidas."
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form, 'error': error})


class UsuarioPasswordResetView(PasswordResetView):
    form_class = ValidatedPasswordResetForm

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def es_administrador(user): # Verifica si el usuario tiene rol de administrador
    return user.is_authenticated and user.rol == 'administrador' # Devuelve True si está autenticado y es admin
@user_passes_test(es_administrador) # Solo permite acceso a administradores
def usuario_list(request): # Muestra la lista de usuarios
    usuarios = Usuario.objects.all() # Obtiene todos los registros de usuarios
    return render(request, 'registration/usuario_list.html', {'usuarios': usuarios})

@user_passes_test(es_administrador) # Solo permite acceso a administradores
def usuario_create(request): # Crea un nuevo usuario
    if request.method == 'POST': # Si se envía el formulario (POST)
        form = UsuarioForm(request.POST) # Carga los datos en el formulario
        if form.is_valid(): # Verifica que los datos sean válidos
            form.save() # Guarda el nuevo usuario en la base de datos
            return redirect('usuario_list') # Redirige a la lista de usuarios
    else: # Si la solicitud es GET
        form = UsuarioForm() # Crea un formulario vacío
    return render(request, 'registration/usuario_form.html', {'form': form}) # Muestra la plantilla del formulario

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
    return redirect('usuario_list')
