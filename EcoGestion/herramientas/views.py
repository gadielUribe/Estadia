from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Herramienta, AsignacionHerramienta
from .forms import HerramientaForm, AsignacionHerramientaForm
from mantenimiento.models import TareaMantenimiento


# _is_admin(user): valida si el usuario es administrador o gestor.
# Entrada: user (objeto User). Salida: True si tiene permisos de administrador.
def _is_admin(user):
    # Para este módulo, administrador y gestor tienen permisos completos
    return user.is_authenticated and getattr(user, 'rol', '') in ('administrador', 'gestor')


# _is_registrador(user): comprueba si el usuario puede registrar/editar herramientas.
# Entrada: user (objeto User). Salida: True si es admin o gestor.
def _is_registrador(user):
    return user.is_authenticated and getattr(user, 'rol', '') in ('administrador', 'gestor')


@login_required
# herramienta_list(request): lista todas las herramientas disponibles.
# Entrada: request (HttpRequest). Salida: HttpResponse con plantilla de listado.
def herramienta_list(request):
    herramientas = Herramienta.objects.all()
    return render(request, 'herramientas/list.html', {"herramientas": herramientas, "section": "herramientas"})


@login_required
@user_passes_test(_is_registrador)
# herramienta_create(request): crea una nueva herramienta en el inventario.
# Entrada: request (HttpRequest). Salida: redirección al listado o formulario con errores.
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
# herramienta_update(request, pk): edita la información de una herramienta existente.
# Entrada: request (HttpRequest), pk (clave primaria).
# Salida: redirección al listado o recarga del formulario.
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
# herramienta_delete(request, pk): elimina una herramienta seleccionada.
# Entrada: request (HttpRequest), pk (identificador de la herramienta).
# Salida: redirección al listado tras confirmar.
def herramienta_delete(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    if request.method == 'POST':
        herramienta.delete()
        return redirect('herramientas:herramienta_list')
    return render(request, 'herramientas/confirm_delete.html', {"herramienta": herramienta, "section": "herramientas"})


@login_required
@user_passes_test(_is_registrador)
# asignar_herramienta(request): asigna una herramienta a una tarea.
# Entrada: request (HttpRequest). Salida: redirección a lista de asignaciones o formulario con errores.
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
# asignacion_list(request): muestra la lista de asignaciones de herramientas.
# Entrada: request (HttpRequest). Salida: HttpResponse con la tabla de asignaciones.
def asignacion_list(request):
    asignaciones = AsignacionHerramienta.objects.select_related('herramienta', 'asignado_por').all()
    return render(request, 'herramientas/asignaciones.html', {"asignaciones": asignaciones, "section": "herramientas"})


@login_required
@user_passes_test(_is_registrador)
# asignacion_delete(request, pk): elimina una asignación de herramienta.
# Entrada: request (HttpRequest), pk (id de la asignación). Salida: redirección.
def asignacion_delete(request, pk):
    asignacion = get_object_or_404(AsignacionHerramienta, pk=pk)
    
    if request.method == 'POST':
        asignacion.delete()
        return redirect('herramientas:herramienta_list')
        
    # Si se accede por GET, simplemente redirige
    return redirect('herramientas:herramienta_list')


@login_required
# herramienta_tareas(request, pk): muestra las tareas vinculadas a una herramienta.
# Entrada: request (HttpRequest), pk (id de la herramienta). Salida: HttpResponse con la lista de tareas.
def herramienta_tareas(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    tareas = (
        TareaMantenimiento.objects.select_related('planta', 'usuario_responsable')
        .filter(herramienta=herramienta)
        .order_by('-fecha_programada')
    )
    return render(
        request,
        'herramientas/tareas_herramienta.html',
        {
            'herramienta': herramienta,
            'tareas': tareas,
            'section': 'herramientas',
        },
    )
