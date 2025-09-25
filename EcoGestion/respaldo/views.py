import io
import os
from pathlib import Path
from datetime import datetime, timezone as dt_timezone
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.management import call_command
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

def _backup_dir() -> Path:
    # Intenta leer desde DBBACKUP_STORAGE_OPTIONS si lo usas
    opts = getattr(settings, 'DBBACKUP_STORAGE_OPTIONS', None)
    if isinstance(opts, dict) and 'location' in opts:
        return Path(opts['location'])
    # Si usas STORAGES con alias 'dbbackup'
    storages = getattr(settings, 'STORAGES', {})
    dbb = storages.get('dbbackup', {})
    opts = dbb.get('OPTIONS', {})
    if 'location' in opts:
        return Path(opts['location'])
    # Fallback
    return Path(settings.BASE_DIR) / 'backups'

def _list_backups():
    d = _backup_dir()
    if not d.exists():
        return []
    files = [f for f in d.iterdir() if f.is_file()]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files

def _is_staff(user):
    return user.is_active and user.is_staff

@login_required
@user_passes_test(_is_staff)
def panel_respaldos(request):
    files_info = []
    for f in _list_backups():
        stat = f.stat()
        # epoch (UTC) -> datetime aware UTC -> a tu zona (settings.TIME_ZONE)
        mtime_local = timezone.localtime(
            datetime.fromtimestamp(stat.st_mtime, tz=dt_timezone.utc)
        )
        files_info.append({
            'name': f.name,
            'size': stat.st_size,
            'mtime_str': mtime_local.strftime('%Y-%m-%d %H:%M'),
        })
    return render(request, 'respaldo/inicio.html', {'files': files_info})

@login_required
@user_passes_test(_is_staff)
@require_POST
def backup_now(request):
    # Crea un respaldo usando django-dbbackup
    out = io.StringIO()
    try:
        call_command('dbbackup', stdout=out)
        messages.success(request, 'Respaldo creado correctamente.')
    except Exception as e:
        messages.error(request, f'Error al crear respaldo: {e}')
    return redirect('respaldo_inicio')

@login_required
@user_passes_test(_is_staff)
@require_POST
def restore_latest(request):
    files = _list_backups()
    if not files:
        messages.error(request, 'No hay archivos de respaldo.')
        return redirect('respaldo_inicio')

    latest = files[0]
    return _restore_common(request, latest.name)

@login_required
@user_passes_test(_is_staff)
@require_POST
def restore_file(request, filename):
    return _restore_common(request, filename)

def _restore_common(request, filename: str):
    out = io.StringIO()
    try:
        
        # call_command('dbrestore', interactive=False, input_filename=filename, uncompress=True, stdout=out)
        call_command('dbrestore', interactive=False, input_filename=filename, stdout=out)

        messages.success(request, f'Restauración completada desde: {filename}')
    except Exception as e:
        messages.error(request, f'Error al restaurar {filename}: {e}')
    return redirect('respaldo_inicio')

@login_required
@user_passes_test(_is_staff)
def download_backup(request, filename):
    path = _backup_dir() / filename
    if not (path.exists() and path.is_file()):
        raise Http404('Archivo no encontrado')
    return FileResponse(open(path, 'rb'), as_attachment=True, filename=filename)

@login_required
@user_passes_test(_is_staff)
@require_POST
def upload_backup(request):
    file = request.FILES.get('file')
    if not file:
        messages.error(request, 'Selecciona un archivo.')
        return redirect('respaldo_inicio')

    dest = _backup_dir()
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / file.name
    with open(target, 'wb+') as dst:
        for chunk in file.chunks():
            dst.write(chunk)
    messages.success(request, f'Archivo {file.name} subido a {dest}.')
    return redirect('respaldo_inicio')
