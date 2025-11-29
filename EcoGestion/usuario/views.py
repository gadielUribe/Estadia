from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Usuario
from .forms import LoginForm, UsuarioForm, ValidatedPasswordResetForm

# user_login(request): procesa el inicio de sesión de un usuario.
# Entrada: request (HttpRequest con datos del formulario).
# Salida: HttpResponse con el formulario o redirección al dashboard si las credenciales son válidas.
def user_login(request):
    error = None  # Variable para almacenar mensaje de error
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Carga los datos enviados en el formulario
        if form.is_valid():
            matricula = form.cleaned_data['matricula']
            password = form.cleaned_data['password']
            # Autentica al usuario usando la matrícula y contraseña
            user = authenticate(request, matricula=matricula, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error = "Credenciales inválidas."
    else:
        form = LoginForm()  # Crea un formulario de login vacío
    return render(request, 'registration/login.html', {'form': form, 'error': error})

# UsuarioPasswordResetView: vista para solicitar el restablecimiento de contraseña.
# Entrada: Request del usuario que solicita restablecer su contraseña.
# Salida: formulario de correo electrónico para enviar el enlace de recuperación.
class UsuarioPasswordResetView(PasswordResetView):
    form_class = ValidatedPasswordResetForm
@login_required
# dashboard(request): muestra la página principal del usuario autenticado.
# Entrada: request (HttpRequest). Salida: HttpResponse con la plantilla del panel principal.
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

# es_administrador(user): verifica si el usuario tiene rol administrador.
# Entrada: user (objeto User autenticado). Salida: True si es administrador, False en caso contrario.
def es_administrador(user): 
    return user.is_authenticated and user.rol == 'administrador' 
@user_passes_test(es_administrador) # Solo permite acceso a administradores

# usuario_list(request): muestra la lista de usuarios registrados.
# Entrada: request (HttpRequest). Salida: HttpResponse con la plantilla de lista de usuarios.
def usuario_list(request): 
    usuarios = Usuario.objects.all() # Obtiene todos los registros de usuarios
    return render(request, 'registration/usuario_list.html', {'usuarios': usuarios})

@user_passes_test(es_administrador) # Solo permite acceso a administradores

# usuario_create(request): registra un nuevo usuario en el sistema.
# Entrada: request (HttpRequest). Salida: redirección a la lista de usuarios o formulario con errores.
def usuario_create(request): 
    if request.method == 'POST': 
        form = UsuarioForm(request.POST) # Carga los datos en el formulario
        if form.is_valid(): 
            form.save() 
            return redirect('usuario_list') # Redirige a la lista de usuarios
    else: 
        form = UsuarioForm() # Crea un formulario vacío
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
    return redirect('usuario_list')
