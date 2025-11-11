from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

from mantenimiento.models import TareaMantenimiento
from notificaciones.signals import notificar


class Command(BaseCommand):
    help = "Envía recordatorios 24h antes de vencer tareas de mantenimiento"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="No enviar, solo mostrar")

    def handle(self, *args, **opts):
        now = timezone.now()
        window_end = now + timedelta(hours=24)

        qs = (
            TareaMantenimiento.objects.select_related("planta", "usuario_responsable")
            .filter(
                estado=TareaMantenimiento.ESTADO_PENDIENTE,
                usuario_responsable__isnull=False,
                fecha_programada__gt=now,
                fecha_programada__lte=window_end,
                recordatorio_24h_enviado=False,
            )
        )

        count = 0
        for tarea in qs:
            user = tarea.usuario_responsable
            if not user:
                continue

            asunto = f"Recordatorio: {tarea.get_tipo_display()} para {tarea.planta.nombre_comun}"
            fecha_local = timezone.localtime(tarea.fecha_programada).strftime("%Y-%m-%d %H:%M")
            cuerpo = (
                f"Hola {getattr(user, 'nombre_completo', user.matricula)},\n\n"
                f"Tienes programada una tarea de {tarea.get_tipo_display()} para la planta/árbol '{tarea.planta.nombre_comun}'.\n"
                f"Fecha y hora programada: {fecha_local}.\n\n"
                f"Por favor, recuerda realizarla y marcarla como realizada en el sistema.\n"
            )

            if opts["dry_run"]:
                self.stdout.write(f"[DRY] Notificar a {user.email}: {asunto}")
            else:
                # Notificación web
                try:
                    notificar.send(
                        sender=tarea,
                        destiny=user,
                        verbo=asunto,
                        target=tarea,
                        level="warning",
                    )
                except Exception as e:
                    self.stderr.write(f"Error notificación web: {e}")

                # Correo
                try:
                    if getattr(settings, "EMAIL_HOST_USER", None):
                        send_mail(asunto, cuerpo, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
                except Exception as e:
                    self.stderr.write(f"Error envío correo: {e}")

                # Marcar que ya se envió recordatorio
                tarea.recordatorio_24h_enviado = True
                tarea.save(update_fields=["recordatorio_24h_enviado", "actualizado_en"])

                count += 1

        self.stdout.write(self.style.SUCCESS(f"Recordatorios enviados: {count}"))
