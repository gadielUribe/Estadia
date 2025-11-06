from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from notificaciones.signals import notificar
from django.db.models import Q
from django.http import HttpResponse
from django.utils.timezone import localtime

from .models import SaludRegistro, SaludHistorial
from .forms import SaludForm

def es_admin_o_gestor(user):
    return user.is_authenticated and getattr(user, "rol", None) in ["administrador", "gestor"]

def es_admin_gestor_mantenimiento(user):
    return user.is_authenticated and getattr(user, "rol", None) in ["administrador", "gestor", "mantenimiento"]

def _parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None

@login_required
@user_passes_test(es_admin_gestor_mantenimiento)
def inicio(request):
    qs = SaludRegistro.objects.select_related('planta', 'usuario')

    q = (request.GET.get('q') or '').strip()
    estado = (request.GET.get('estado') or '').strip()
    f_from = request.GET.get('desde') or ''
    f_to = request.GET.get('hasta') or ''
    planta_id = request.GET.get('planta') or ''
    usuario_id = request.GET.get('usuario') or ''

    if q:
        qs = qs.filter(
            Q(planta__nombre_comun__icontains=q) |
            Q(planta__nombre_cientifico__icontains=q) 
        )
    if estado in {'verde','amarillo','rojo'}:
        qs = qs.filter(estado_salud=estado)
    d_from = _parse_date(f_from)
    d_to = _parse_date(f_to)
    if d_from:
        qs = qs.filter(fecha_actualizacion__date__gte=d_from)
    if d_to:
        qs = qs.filter(fecha_actualizacion__date__lte=d_to)
    if planta_id.isdigit():
        qs = qs.filter(planta_id=int(planta_id))
    if usuario_id.isdigit():
        qs = qs.filter(usuario_id=int(usuario_id))

    registros = qs.order_by('-fecha_actualizacion', '-id_registro')

    ctx = {
        'registros': registros[:300],
        'q': q, 'estado': estado, 'desde': f_from, 'hasta': f_to,
        'planta_id': planta_id, 'usuario_id': usuario_id,
        'total': qs.count(),
    }
    return render(request, 'salud/read.html', ctx)

@login_required
@user_passes_test(es_admin_o_gestor)
def crear(request):
    if request.method == 'POST':
        form = SaludForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario = request.user
            obj.save()

            # registrar historial inicial
            SaludHistorial.objects.create(
                planta=obj.planta,
                usuario=request.user,
                estado_salud=obj.estado_salud,
                observaciones=obj.observaciones,
            )

            _notificar_si_riesgo(obj)
            return redirect('salud_inicio')
    else:
        form = SaludForm()
    return render(request, 'salud/create.html', {'form': form})

@login_required
@user_passes_test(es_admin_o_gestor)
def editar(request, id_registro):
    reg = get_object_or_404(SaludRegistro, pk=id_registro)
    if request.method == 'POST':
        form = SaludForm(request.POST, instance=reg)
        form.fields['planta'].required = False
        form.fields['planta'].disabled = True

        if form.is_valid():
            obj = form.save(commit=False)
            obj.planta = reg.planta
            obj.usuario = request.user
            obj.save()

            # registrar historial cada vez que se edita
            SaludHistorial.objects.create(
                planta=obj.planta,
                usuario=request.user,
                estado_salud=obj.estado_salud,
                observaciones=obj.observaciones,
            )

            _notificar_si_riesgo(obj)
            return redirect('salud_inicio')
    else:
        form = SaludForm(instance=reg)
        form.fields['planta'].disabled = True

    return render(request, 'salud/update.html', {'form': form, 'registro': reg})

@login_required
@user_passes_test(es_admin_o_gestor)
def eliminar(request, id_registro):
    reg = get_object_or_404(SaludRegistro, pk=id_registro)
    if request.method == 'POST':
        reg.delete()
        return redirect('salud_inicio')
    return render(request, 'salud/delete.html', {'registro': reg})

def _notificar_si_riesgo(reg: SaludRegistro):
    # solo notificamos si es amarillo o rojo
    if reg.estado_salud not in ('amarillo', 'rojo'):
        return

    User = get_user_model()
    # todos los admins (ajusta si tu campo se llama distinto)
    admins = User.objects.filter(rol='administrador', is_active=True)

    # por si no hay admins, no truena
    if not admins.exists():
        return

    # mensaje de la notificación
    mensaje = (
        f"La planta '{reg.planta}' fue registrada con estado '{reg.estado_salud}'. "
        "Requiere atención prioritaria."
    )

    # nivel según color
    nivel = 'Atencion' if reg.estado_salud == 'amarillo' else 'Peligro'

    # enviamos una notificación por admin
    for admin in admins:
        notificar.send(
            sender=reg.usuario,        # quién hizo el cambio (el que registró la salud)
            destiny=admin,             # a quién le llega (admin)
            verbo=mensaje,
            target=reg.planta,         
            level=nivel,
        )

@login_required
@user_passes_test(es_admin_gestor_mantenimiento)
def historial_planta(request, planta_id):
    from plantas.models import plantaArbol
    planta = get_object_or_404(plantaArbol, pk=planta_id)

    eventos = (SaludHistorial.objects
               .select_related('usuario')
               .filter(planta_id=planta_id)
               .order_by('-fecha_evento'))

    ctx = {
        'planta': planta,
        'eventos': eventos,
        'total': eventos.count(),
    }
    return render(request, 'salud/historial_planta.html', ctx)