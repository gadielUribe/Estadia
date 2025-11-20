from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from mantenimiento.models import TareaMantenimiento
from notificaciones.signals import notificar


class Command(BaseCommand):
    help = "Envía recordatorios 24h antes y alertas cuando una tarea vence sin completarse."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="No enviar, solo mostrar")

    def handle(self, *args, **opts):
        self.dry_run = opts["dry_run"]
        now = timezone.now()

        enviados_recordatorios = self._enviar_recordatorios_24h(now)
        enviados_vencidas = self._enviar_alertas_vencidas(now)

        msg = (
            f"Recordatorios 24h enviados: {enviados_recordatorios} | "
            f"Alertas de vencimiento enviadas: {enviados_vencidas}"
        )
        self.stdout.write(self.style.SUCCESS(msg))

    # Helpers
    def _nombre_usuario(self, user):
        return getattr(user, "nombre_completo", None) or getattr(user, "matricula", "") or user.get_username()

    def _send_notification(self, tarea, user, asunto, cuerpo, level, update_fields):
        if self.dry_run:
            self.stdout.write(f"[DRY] Notificar a {user.email}: {asunto}")
            return False

        # Notificación en plataforma
        try:
            notificar.send(
                sender=tarea,
                destiny=user,
                verbo=asunto,
                target=tarea,
                level=level,
            )
        except Exception as e:
            self.stderr.write(f"Error notificación web: {e}")

        # Correo electrónico
        try:
            if getattr(settings, "EMAIL_HOST_USER", None):
                send_mail(asunto, cuerpo, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
        except Exception as e:
            self.stderr.write(f"Error envío correo: {e}")

        # Marcar flags en la tarea
        tarea.save(update_fields=update_fields)
        return True

    def _enviar_recordatorios_24h(self, now):
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
                f"Hola {self._nombre_usuario(user)},\n\n"
                f"Tienes programada una tarea de {tarea.get_tipo_display()} para la planta/árbol '{tarea.planta.nombre_comun}'.\n"
                f"Fecha y hora programada: {fecha_local}.\n\n"
                "Por favor, recuerda realizarla y marcarla como realizada en el sistema.\n"
            )

            tarea.recordatorio_24h_enviado = True
            if self._send_notification(
                tarea,
                user,
                asunto,
                cuerpo,
                level="warning",
                update_fields=["recordatorio_24h_enviado", "actualizado_en"],
            ):
                count += 1

        return count

    def _enviar_alertas_vencidas(self, now):
        qs = (
            TareaMantenimiento.objects.select_related("planta", "usuario_responsable")
            .filter(
                estado=TareaMantenimiento.ESTADO_PENDIENTE,
                usuario_responsable__isnull=False,
                fecha_programada__lte=now,
                vencimiento_notificado=False,
            )
        )

        count = 0
        for tarea in qs:
            user = tarea.usuario_responsable
            if not user:
                continue

            fecha_local = timezone.localtime(tarea.fecha_programada).strftime("%Y-%m-%d %H:%M")
            asunto = f"Tarea vencida: {tarea.get_tipo_display()} para {tarea.planta.nombre_comun}"
            cuerpo = (
                f"Hola {self._nombre_usuario(user)},\n\n"
                f"La tarea de {tarea.get_tipo_display()} asignada a ti para la planta/árbol "
                f"'{tarea.planta.nombre_comun}' venció el {fecha_local} y sigue marcada como pendiente.\n\n"
                "Por favor ingresa a la plataforma para completarla o reprogramarla.\n"
            )

            tarea.vencimiento_notificado = True
            if self._send_notification(
                tarea,
                user,
                asunto,
                cuerpo,
                level="error",
                update_fields=["vencimiento_notificado", "actualizado_en"],
            ):
                count += 1

        return count
