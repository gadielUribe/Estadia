from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Voluntario, AsignacionVoluntario
from .forms import VoluntarioForm


# _is_admin(user): valida si el usuario autenticado tiene rol de administrador.
# Entrada: user (objeto User). Salida: True si es admin, False en caso contrario.
def _is_admin(user):
    return user.is_authenticated and getattr(user, 'rol', '') == 'administrador'


# _is_gestor(user): valida si el usuario tiene rol de administrador o gestor.
# Entrada: user (objeto User). Salida: True si tiene permisos de gestion.
def _is_gestor(user):
    return user.is_authenticated and getattr(user, 'rol', '') in ('administrador', 'gestor')


@login_required
# voluntario_list(request): muestra la lista de voluntarios con filtros por nombre y tipo.
# Entrada: request (HttpRequest con posibles parametros q y tipo).
# Salida: HttpResponse renderizando la plantilla de listado.
def voluntario_list(request):
    q = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    voluntarios = Voluntario.objects.all()
    if q:
        voluntarios = voluntarios.filter(models.Q(nombre__icontains=q) | models.Q(apellido__icontains=q) | models.Q(email__icontains=q))
    if tipo:
        voluntarios = voluntarios.filter(tipo_participacion=tipo)
    return render(request, 'voluntarios/list.html', {'voluntarios': voluntarios, 'q': q, 'tipo': tipo, 'section': 'voluntarios'})


@login_required
@user_passes_test(_is_gestor)
# voluntario_create(request): crea un nuevo voluntario.
# Entrada: request (HttpRequest). Salida: redireccion a listado o formulario con errores.
def voluntario_create(request):
    if request.method == 'POST':
        form = VoluntarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('voluntarios:voluntario_list')
    else:
        form = VoluntarioForm()
    return render(request, 'voluntarios/form.html', {'form': form, 'titulo': 'Nuevo voluntario', 'section': 'voluntarios'})


@login_required
@user_passes_test(_is_gestor)
# voluntario_update(request, pk): edita los datos de un voluntario existente.
# Entrada: request (HttpRequest), pk (clave primaria del voluntario).
# Salida: redireccion a listado o recarga del formulario con errores.
def voluntario_update(request, pk):
    voluntario = get_object_or_404(Voluntario, pk=pk)
    if request.method == 'POST':
        form = VoluntarioForm(request.POST, instance=voluntario)
        if form.is_valid():
            form.save()
            return redirect('voluntarios:voluntario_list')
    else:
        form = VoluntarioForm(instance=voluntario)
    return render(request, 'voluntarios/form.html', {'form': form, 'titulo': 'Editar voluntario', 'section': 'voluntarios'})


@login_required
@user_passes_test(_is_admin)
# voluntario_delete(request, pk): elimina un voluntario de la base de datos.
# Entrada: request (HttpRequest), pk (identificador del voluntario).
# Salida: redireccion al listado tras eliminar.
def voluntario_delete(request, pk):
    voluntario = get_object_or_404(Voluntario, pk=pk)
    if request.method == 'POST':
        voluntario.delete()
        return redirect('voluntarios:voluntario_list')
    return redirect('voluntarios:voluntario_list')


@login_required
# asignacion_list(request): lista todas las asignaciones de voluntarios.
# Entrada: request (HttpRequest). Salida: HttpResponse con la plantilla de asignaciones.
def asignacion_list(request):
    asignaciones = AsignacionVoluntario.objects.select_related('voluntario', 'asignado_por').all()
    return render(request, 'voluntarios/asignaciones.html', {'asignaciones': asignaciones, 'section': 'voluntarios'})


@login_required
@user_passes_test(_is_gestor)
# asignacion_delete(request, pk): elimina una asignacion de voluntario.
# Entrada: request (HttpRequest), pk (identificador de la asignacion).
# Salida: redireccion a la lista de asignaciones.
def asignacion_delete(request, pk):
    asign = get_object_or_404(AsignacionVoluntario, pk=pk)
    if request.method == 'POST':
        asign.delete()
        return redirect('voluntarios:asignacion_list')
    return redirect('voluntarios:asignacion_list')

