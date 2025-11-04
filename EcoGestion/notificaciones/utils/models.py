from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.utils import timezone
from django.conf import settings
from notificaciones.signals import notificar
from swapper import load_model


class NotificacionQuerySet(models.QuerySet):
    def leidas(self, include_deleted=False):
        qs = self.filter(no_leido=False)
        if not include_deleted:
            qs = qs.filter(eliminar=False)
        return qs

    def no_leidas(self, include_deleted=False):
        qs = self.filter(no_leido=True)
        if not include_deleted:
            qs = qs.filter(eliminar=False)
        return qs

    def marcar_todo_como_leido(self, destino=None):
        qs = self.no_leidas(include_deleted=True)
        if destino is not None:
            qs = qs.filter(destiny=destino)
        return qs.update(no_leido=False)

    def marcar_todo_como_no_leido(self, destino=None):
        qs = self.leidas(include_deleted=True)
        if destino is not None:
            qs = qs.filter(destiny=destino)
        return qs.update(no_leido=True)


class AbstractNotificacion(models.Model):

    class Levels(models.TextChoices):
        success = 'success', 'Success'
        info = 'info', 'Info'
        warning = 'warning', 'Warning'
        error = 'error', 'Error'

    level = models.CharField(
        choices=Levels.choices,
        max_length=20,
        default=Levels.info
    )

    # a quién le llega
    destiny = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        blank=True,
        null=True
    )

    # quién hizo la acción
    actor_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='notificar_actor'
    )
    object_id_actor = models.PositiveIntegerField()
    actor = GenericForeignKey('actor_content_type', 'object_id_actor')

    # sobre qué se hizo la acción
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='notificar_target',
        blank=True,
        null=True,
    )
    object_id_target = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey('target_content_type', 'object_id_target')

    verbo = models.CharField(max_length=255)

    no_leido = models.BooleanField(default=True)

    publico = models.BooleanField(default=True)
    eliminar = models.BooleanField(default=False)

    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    objects = NotificacionQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ['-timestamp']


def notify_signals(sender, **kwargs):
    """
    Receiver del signal `notificar`.
    Espera al menos: destiny, verbo
    Opcional: target, level, publico, timestamp
    """
    destiny = kwargs.pop('destiny', None)
    verbo = kwargs.pop('verbo', None) 
    publico = kwargs.pop('publico', True)
    timestamp = kwargs.pop('timestamp', timezone.now())
    target = kwargs.pop('target', None)

    # tu modelo real
    Notify = load_model('notificaciones', 'Notificacion')
    level = kwargs.pop('level', Notify.Levels.info)

    if destiny is None or verbo is None:
        # si no me mandan destino o verbo, no hago nada
        return

    # puede ser un grupo, un queryset o un usuario
    if isinstance(destiny, Group):
        destinies = destiny.user_set.all()
    elif isinstance(destiny, QuerySet):
        destinies = destiny
    else:
        destinies = [destiny]

    nuevas = []
    for dest in destinies:
        noti = Notify(
            destiny=dest,
            actor_content_type=ContentType.objects.get_for_model(sender),
            object_id_actor=sender.pk,
            verbo=verbo,
            publico=publico,
            timestamp=timestamp,
            level=level,
        )

        # si vino un objeto como target, lo guardamos
        if target is not None:
            noti.target_content_type = ContentType.objects.get_for_model(target)
            noti.object_id_target = target.pk

        noti.save()
        nuevas.append(noti)

    return nuevas


# conectar el receiver
notificar.connect(
    notify_signals,
    dispatch_uid="notificaciones.models.notify_signals"
)