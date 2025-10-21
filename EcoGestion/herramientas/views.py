from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Herramienta, AsignacionHerramienta
from .forms import HerramientaForm, AsignacionHerramientaForm


def _is_admin(user):
    return user.is_authenticated and getattr(user, 'rol', '') == 'administrador'


def _is_registrador(user):
    # Usa 'gestor' como registrador por ahora
    return user.is_authenticated and getattr(user, 'rol', '') in ('administrador', 'gestor')


@login_required
def herramienta_list(request):
    herramientas = Herramienta.objects.all()
    return render(request, 'herramientas/list.html', {"herramientas": herramientas, "section": "herramientas"})


@login_required
@user_passes_test(_is_registrador)
def herramienta_create(request):
    if request.method == 'POST':
        form = HerramientaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('herramientas:herramienta_list')
    else:
        form = HerramientaForm()
    return render(request, 'herramientas/form.html', {"form": form, "titulo": "Nueva herramienta", "section": "herramientas"})


@login_required
@user_passes_test(_is_registrador)
def herramienta_update(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    if request.method == 'POST':
        form = HerramientaForm(request.POST, instance=herramienta)
        if form.is_valid():
            form.save()
            return redirect('herramientas:herramienta_list')
    else:
        form = HerramientaForm(instance=herramienta)
    return render(request, 'herramientas/form.html', {"form": form, "titulo": "Editar herramienta", "section": "herramientas"})


@login_required
@user_passes_test(_is_admin)
def herramienta_delete(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    if request.method == 'POST':
        herramienta.delete()
        return redirect('herramientas:herramienta_list')
    return render(request, 'herramientas/confirm_delete.html', {"herramienta": herramienta, "section": "herramientas"})


@login_required
@user_passes_test(_is_registrador)
def asignar_herramienta(request):
    if request.method == 'POST':
        form = AsignacionHerramientaForm(request.POST)
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.asignado_por = request.user
            asignacion.save()
            return redirect('herramientas:asignacion_list')
    else:
        form = AsignacionHerramientaForm()
    return render(request, 'herramientas/asignar.html', {"form": form, "section": "herramientas"})


@login_required
def asignacion_list(request):
    asignaciones = AsignacionHerramienta.objects.select_related('herramienta', 'asignado_por').all()
    return render(request, 'herramientas/asignaciones.html', {"asignaciones": asignaciones, "section": "herramientas"})


@login_required
@user_passes_test(_is_registrador)
def asignacion_delete(request, pk):
    asignacion = get_object_or_404(AsignacionHerramienta, pk=pk)
    if request.method == 'POST':
        asignacion.delete()
        return redirect('herramientas:asignacion_list')
    return render(request, 'herramientas/confirm_delete_asignacion.html', {"asignacion": asignacion, "section": "herramientas"})
