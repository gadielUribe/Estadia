from django.db import models
from notificaciones.utils.models import AbstractNotificacion

# Create your models here.
class Notificacion(AbstractNotificacion):
    pass

    class Meta(AbstractNotificacion.Meta):
        abstract = False