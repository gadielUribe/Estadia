from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Voluntario, AsignacionVoluntario
from .forms import VoluntarioForm, AsignacionVoluntarioForm


def _is_admin(user):
    return user.is_authenticated and getattr(user, 'rol', '') == 'administrador'


def _is_gestor(user):
    return user.is_authenticated and getattr(user, 'rol', '') in ('administrador', 'gestor')


@login_required
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
def voluntario_create(request):
    if request.method == 'POST':
        form = VoluntarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Voluntario registrado.')
            return redirect('voluntarios:voluntario_list')
    else:
        form = VoluntarioForm()
    return render(request, 'voluntarios/form.html', {'form': form, 'titulo': 'Nuevo voluntario', 'section': 'voluntarios'})


@login_required
@user_passes_test(_is_gestor)
def voluntario_update(request, pk):
    voluntario = get_object_or_404(Voluntario, pk=pk)
    if request.method == 'POST':
        form = VoluntarioForm(request.POST, instance=voluntario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Voluntario actualizado.')
            return redirect('voluntarios:voluntario_list')
    else:
        form = VoluntarioForm(instance=voluntario)
    return render(request, 'voluntarios/form.html', {'form': form, 'titulo': 'Editar voluntario', 'section': 'voluntarios'})


@login_required
@user_passes_test(_is_admin)
def voluntario_delete(request, pk):
    voluntario = get_object_or_404(Voluntario, pk=pk)
    if request.method == 'POST':
        voluntario.delete()
        messages.success(request, 'Voluntario eliminado.')
        return redirect('voluntarios:voluntario_list')
    return render(request, 'voluntarios/confirm_delete.html', {'voluntario': voluntario, 'section': 'voluntarios'})


@login_required
@user_passes_test(_is_gestor)
def asignar_voluntario(request):
    if request.method == 'POST':
        form = AsignacionVoluntarioForm(request.POST)
        if form.is_valid():
            asign = form.save(commit=False)
            asign.asignado_por = request.user
            asign.save()
            messages.success(request, 'Voluntario asignado a actividad/evento.')
            return redirect('voluntarios:asignacion_list')
    else:
        form = AsignacionVoluntarioForm()
    return render(request, 'voluntarios/asignar.html', {'form': form, 'section': 'voluntarios'})


@login_required
def asignacion_list(request):
    asignaciones = AsignacionVoluntario.objects.select_related('voluntario', 'asignado_por').all()
    return render(request, 'voluntarios/asignaciones.html', {'asignaciones': asignaciones, 'section': 'voluntarios'})


@login_required
@user_passes_test(_is_gestor)
def asignacion_delete(request, pk):
    asign = get_object_or_404(AsignacionVoluntario, pk=pk)
    if request.method == 'POST':
        asign.delete()
        messages.success(request, 'Asignación eliminada.')
        return redirect('voluntarios:asignacion_list')
    return render(request, 'voluntarios/confirm_delete_asignacion.html', {'asignacion': asign, 'section': 'voluntarios'})

