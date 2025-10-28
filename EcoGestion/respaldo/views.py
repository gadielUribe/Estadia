import io
import os
import shlex
import subprocess
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

from .models import BackupAudit


def _backup_dir() -> Path:
    opts = getattr(settings, 'DBBACKUP_STORAGE_OPTIONS', None)
    if isinstance(opts, dict) and 'location' in opts:
        return Path(opts['location'])
    storages = getattr(settings, 'STORAGES', {})
    dbb = storages.get('dbbackup', {})
    opts = dbb.get('OPTIONS', {})
    if 'location' in opts:
        return Path(opts['location'])
    return Path(settings.BASE_DIR) / 'backups'


def _list_backups():
    d = _backup_dir()
    if not d.exists():
        return []
    files = [f for f in d.iterdir() if f.is_file() and f.suffix.lower() == '.sql']
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def _is_staff(user):
    return user.is_authenticated and getattr(user, "rol", None) in ["administrador"]


def _db_conf():
    cfg = settings.DATABASES['default']
    NAME = cfg.get('NAME')
    USER = cfg.get('USER') or ''
    PASSWORD = cfg.get('PASSWORD') or ''
    HOST = cfg.get('HOST') or '127.0.0.1'
    PORT = str(cfg.get('PORT') or '3306')
    ENGINE = cfg.get('ENGINE', '')
    is_mysql = 'mysql' in ENGINE  # mysqlclient / mariadb
    return {'NAME': NAME, 'USER': USER, 'PASSWORD': PASSWORD, 'HOST': HOST, 'PORT': PORT, 'IS_MYSQL': is_mysql}


def _maybe_ssl_flag_for_mysql():
    """
    Evita romper si el cliente no reconoce --ssl-mode.
    Devuelve lista de flags seguros (vacía por default).
    """
    # Si tu cliente soporta --ssl-mode, puedes devolver ["--ssl-mode=DISABLED"]
    # pero como en tus logs dio error, lo dejamos vacío para compatibilidad.
    return []


@login_required
@user_passes_test(_is_staff)
def panel_respaldos(request):
    files_info = []
    for f in _list_backups():
        stat = f.stat()
        mtime_local = timezone.localtime(
            datetime.fromtimestamp(stat.st_mtime, tz=dt_timezone.utc)
        )
        files_info.append({
            'name': f.name,
            'size': stat.st_size,
            'mtime_str': mtime_local.strftime('%Y-%m-%d %H:%M'),
        })

    # Últimos eventos de auditoría (opcional: limita a 200)
    audits = BackupAudit.objects.all()[:200]

    return render(request, 'respaldo/inicio.html', {
        'files': files_info,
        'audits': audits,
    })


@login_required
@user_passes_test(_is_staff)
@require_POST
def backup_now(request):
    """
    Genera archivo .sql con mysqldump (para MySQL/MariaDB).
    Si no es MySQL, cae al comando 'dbbackup' como fallback.
    """
    cfg = _db_conf()
    dest = _backup_dir()
    dest.mkdir(parents=True, exist_ok=True)

    ts = timezone.localtime().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{cfg['NAME']}_{ts}.sql"
    outfile = dest / filename
    log_text = io.StringIO()

    if cfg['IS_MYSQL']:
        cmd = [
            'mysqldump',
            '-h', cfg['HOST'],
            '-P', cfg['PORT'],
            '-u', cfg['USER'],
            '--single-transaction',
            '--routines',
            '--events',
            cfg['NAME'],
            *(_maybe_ssl_flag_for_mysql()),
        ]
        # Nota: -pPASSWORD sin espacio para evitar prompt interactivo
        if cfg['PASSWORD']:
            cmd.insert(cmd.index('--single-transaction'), f"-p{cfg['PASSWORD']}")

        try:
            with open(outfile, 'wb') as f:
                proc = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, check=False)
            if proc.returncode == 0:
                messages.success(request, f'Respaldo creado: {filename}')
                log_text.write("OK mysqldump\n")
            else:
                # Borra archivo incompleto
                if outfile.exists():
                    outfile.unlink(missing_ok=True)
                err = proc.stderr.decode(errors='replace')
                messages.error(request, f'Error al crear respaldo (.sql): {err}')
                log_text.write(f"ERROR mysqldump:\n{err}\n")
        except FileNotFoundError:
            messages.error(request, 'mysqldump no está instalado o no está en PATH.')
            log_text.write("ERROR: mysqldump no encontrado\n")
        finally:
            BackupAudit.objects.create(
                action='BACKUP',
                filename=filename,
                user=request.user,
                log=log_text.getvalue()
            )

    else:
        # Fallback para otros motores: usa django-dbbackup (no .sql “puro”)
        out = io.StringIO()
        try:
            call_command('dbbackup', stdout=out)
            messages.success(request, 'Respaldo creado con django-dbbackup.')
            log = f"dbbackup output:\n{out.getvalue()}"
        except Exception as e:
            messages.error(request, f'Error al crear respaldo: {e}')
            log = f"dbbackup ERROR: {e}"
        finally:
            BackupAudit.objects.create(
                action='BACKUP',
                filename='(dbbackup)',
                user=request.user,
                log=log
            )

    return redirect('respaldo_inicio')


@login_required
@user_passes_test(_is_staff)
@require_POST
def restore_latest(request):
    files = _list_backups()
    if not files:
        messages.error(request, 'No hay archivos .sql en la carpeta de respaldos.')
        return redirect('respaldo_inicio')
    latest = files[0]
    return _restore_common(request, latest.name)


@login_required
@user_passes_test(_is_staff)
@require_POST
def restore_file(request, filename):
    return _restore_common(request, filename)


def _restore_common(request, filename: str):
    cfg = _db_conf()
    path = _backup_dir() / filename
    log_text = io.StringIO()

    if not (path.exists() and path.is_file()):
        messages.error(request, f'Archivo no encontrado: {filename}')
        BackupAudit.objects.create(
            action='RESTORE',
            filename=filename,
            user=request.user,
            log='ERROR: archivo no existe'
        )
        return redirect('respaldo_inicio')

    if cfg['IS_MYSQL'] and path.suffix.lower() == '.sql':
        cmd = [
            'mysql',
            '-h', cfg['HOST'],
            '-P', cfg['PORT'],
            '-u', cfg['USER'],
            cfg['NAME'],
            *(_maybe_ssl_flag_for_mysql()),
        ]
        if cfg['PASSWORD']:
            cmd.insert(cmd.index(cfg['NAME']), f"-p{cfg['PASSWORD']}")

        try:
            with open(path, 'rb') as f:
                proc = subprocess.run(cmd, stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            if proc.returncode == 0:
                messages.success(request, f'Restauración completada desde: {filename}')
                log_text.write("OK mysql restore\n")
            else:
                err = proc.stderr.decode(errors='replace')
                messages.error(request, f'Error al restaurar {filename}: {err}')
                log_text.write(f"ERROR mysql restore:\n{err}\n")
        except FileNotFoundError:
            messages.error(request, 'mysql no está instalado o no está en PATH.')
            log_text.write("ERROR: cliente mysql no encontrado\n")
        finally:
            BackupAudit.objects.create(
                action='RESTORE',
                filename=filename,
                user=request.user,
                log=log_text.getvalue()
            )

    else:
        # Fallback a dbrestore (si no es MySQL o extensión no es .sql)
        out = io.StringIO()
        try:
            call_command('dbrestore', interactive=False, input_filename=filename, stdout=out)
            messages.success(request, f'Restauración (dbrestore) desde: {filename}')
            log = f"dbrestore output:\n{out.getvalue()}"
        except Exception as e:
            messages.error(request, f'Error al restaurar {filename}: {e}')
            log = f"dbrestore ERROR: {e}"
        finally:
            BackupAudit.objects.create(
                action='RESTORE',
                filename=filename,
                user=request.user,
                log=log
            )

    return redirect('respaldo_inicio')


@login_required
@user_passes_test(_is_staff)
def download_backup(request, filename):
    path = _backup_dir() / filename
    if not (path.exists() and path.is_file()):
        raise Http404('Archivo no encontrado')
    # Registrar descarga (opcional)
    BackupAudit.objects.create(
        action='DOWNLOAD',
        filename=filename,
        user=request.user,
        log='Descarga iniciada'
    )
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

    # Opcional: exigir .sql
    if not file.name.lower().endswith('.sql'):
        messages.error(request, 'Sólo se permiten archivos .sql')
        return redirect('respaldo_inicio')

    with open(target, 'wb+') as dst:
        for chunk in file.chunks():
            dst.write(chunk)

    messages.success(request, f'Archivo {file.name} subido a {dest}.')
    BackupAudit.objects.create(
        action='UPLOAD',
        filename=file.name,
        user=request.user,
        log='Archivo subido al directorio de respaldos.'
    )
    return redirect('respaldo_inicio')
