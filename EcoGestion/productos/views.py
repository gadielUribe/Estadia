from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction

from .models import Producto, AsignacionProducto
from .forms import ProductoForm, StockUpdateForm, AsignacionProductoForm
from mantenimiento.models import TareaMantenimiento


def _is_admin(user):
    return user.is_authenticated and getattr(user, 'rol', '') == 'administrador'


def _is_registrador(user):
    return user.is_authenticated and getattr(user, 'rol', '') in ('administrador', 'gestor')


@login_required
def producto_list(request):
    q = request.GET.get('q', '').strip()
    productos = Producto.objects.all()
    if q:
        productos = productos.filter(nombre__icontains=q)
    return render(request, 'productos/list.html', {
        'productos': productos,
        'q': q,
        'section': 'productos',
    })


@login_required
@user_passes_test(_is_registrador)
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos:producto_list')
    else:
        form = ProductoForm()
    return render(request, 'productos/form.html', {'form': form, 'titulo': 'Nuevo producto', 'section': 'productos'})


@login_required
@user_passes_test(_is_registrador)
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos:producto_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/form.html', {'form': form, 'titulo': 'Editar producto', 'section': 'productos'})


@login_required
@user_passes_test(_is_admin)
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos:producto_list')
    return render(request, 'productos/confirm_delete.html', {'producto': producto, 'section': 'productos'})


@login_required
@user_passes_test(_is_registrador)
def producto_stock_update(request, pk):
    from .models import Existencia
    producto = get_object_or_404(Producto, pk=pk)
    existencia, _ = Existencia.objects.get_or_create(producto=producto, defaults={'cantidad': 0})
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=existencia)
        if form.is_valid():
            form.save()
            return redirect('productos:producto_list')
    else:
        form = StockUpdateForm(instance=existencia)
    return render(request, 'productos/stock_form.html', {'form': form, 'producto': producto, 'section': 'productos'})


@login_required
@user_passes_test(_is_registrador)
@transaction.atomic
def asignar_producto(request):
    if request.method == 'POST':
        form = AsignacionProductoForm(request.POST)
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.asignado_por = request.user
            producto = asignacion.producto
            from .models import Existencia
            existencia, _ = Existencia.objects.get_or_create(producto=producto, defaults={'cantidad': 0})
            if asignacion.cantidad > existencia.cantidad:
                form.add_error('cantidad', 'Cantidad mayor a existencias disponibles.')
            else:
                existencia.cantidad -= asignacion.cantidad
                existencia.save()
                asignacion.save()
                return redirect('productos:asignacion_list')
    else:
        form = AsignacionProductoForm()
    return render(request, 'productos/asignar.html', {'form': form, 'section': 'productos'})


@login_required
def asignacion_list(request):
    asignaciones = AsignacionProducto.objects.select_related('producto', 'asignado_por').all()
    return render(request, 'productos/asignaciones.html', {'asignaciones': asignaciones, 'section': 'productos'})


@login_required
@user_passes_test(_is_registrador)
@transaction.atomic
def asignacion_delete(request, pk):
    asignacion = get_object_or_404(AsignacionProducto, pk=pk)
    
    if request.method == 'POST':
        # Restituir existencias al eliminar la asignación
        prod = asignacion.producto
        from .models import Existencia
        existencia, _ = Existencia.objects.get_or_create(producto=prod, defaults={'cantidad': 0})
        existencia.cantidad += asignacion.cantidad
        existencia.save()
        
        asignacion.delete()
        return redirect('productos:asignacion_list')

    # --- ESTE ES EL CAMBIO ---
    # Si la petición es GET, ya no mostramos una página.
    # Simplemente redirigimos a la lista, porque el modal se encarga de la confirmación.
    return redirect('productos:asignacion_list')


@login_required
def producto_tareas(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    tareas = (
        TareaMantenimiento.objects.select_related('planta', 'usuario_responsable')
        .filter(producto=producto)
        .order_by('-fecha_programada')
    )
    return render(
        request,
        'productos/tareas_producto.html',
        {
            'producto': producto,
            'tareas': tareas,
            'section': 'productos',
        },
    )
