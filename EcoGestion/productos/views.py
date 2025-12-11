from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.urls import reverse

from .models import Producto, AsignacionProducto
from .forms import ProductoForm, StockUpdateForm, AsignacionProductoForm
from mantenimiento.models import TareaMantenimiento


# _is_admin(user): valida si el usuario es administrador o gestor.
# Entrada: user (objeto User). Salida: True si tiene permisos de eliminación.
def _is_admin(user):
    # Para este módulo, administrador y gestor tienen permisos completos
    return user.is_authenticated and getattr(user, 'rol', '') in ('administrador', 'gestor')


# _is_registrador(user): verifica si el usuario puede crear/editar productos.
# Entrada: user (objeto User). Salida: True si es admin o gestor.
def _is_registrador(user):
    return user.is_authenticated and getattr(user, 'rol', '') in ('administrador', 'gestor')


@login_required
# producto_list(request): lista productos con filtro por nombre.
# Entrada: request (HttpRequest). Salida: HttpResponse con la tabla de productos.
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
# producto_create(request): registra un nuevo producto.
# Entrada: request (HttpRequest). Salida: redirección al listado o formulario con errores.
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
# producto_update(request, pk): edita un producto existente.
# Entrada: request (HttpRequest), pk (id del producto). Salida: redirección o recarga del formulario.
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
# producto_delete(request, pk): elimina un producto.
# Entrada: request (HttpRequest), pk (id del producto). Salida: redirección tras borrar.
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos:producto_list')
    return render(request, 'productos/confirm_delete.html', {'producto': producto, 'section': 'productos'})


@login_required
@user_passes_test(_is_registrador)
# producto_stock_update(request, pk): actualiza existencias de un producto.
# Entrada: request (HttpRequest), pk (id del producto). Salida: redirección o formulario con errores.
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
# asignar_producto(request): asigna productos a una tarea descontando existencias.
# Entrada: request (HttpRequest). Salida: redirección a lista de asignaciones o formulario con errores.
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
# asignacion_list(request): lista las asignaciones de productos a tareas.
# Entrada: request (HttpRequest). Salida: HttpResponse con la tabla de asignaciones.
def asignacion_list(request):
    asignaciones = AsignacionProducto.objects.select_related('producto', 'asignado_por').all()
    return render(request, 'productos/asignaciones.html', {'asignaciones': asignaciones, 'section': 'productos'})


@login_required
@user_passes_test(_is_registrador)
@transaction.atomic
# asignacion_delete(request, pk): elimina una asignación y devuelve existencias al stock.
# Entrada: request (HttpRequest), pk (id de la asignación). Salida: redirección.
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


    # Si la petición es GET, ya no mostramos una página.
    # Simplemente redirigimos a la lista, porque el modal se encarga de la confirmación.
    return redirect('productos:asignacion_list')


@login_required
# producto_tareas(request, pk): muestra las tareas donde se usa un producto.
# Entrada: request (HttpRequest), pk (id del producto). Salida: HttpResponse con la lista de tareas.
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


@login_required
def reporte_productos_inventario_redirect(request):
    # Acceso directo al reporte de inventario/movimientos desde el módulo de productos
    # Acceso directo al reporte de inventario/movimientos desde el módulo de productos
    return redirect(reverse("reporte_productos_inventario"))
