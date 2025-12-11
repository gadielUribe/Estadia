from django.db import models
from notificaciones.utils.models import AbstractNotificacion

# Notificacion: implementacion concreta del modelo abstracto de notificaciones.
# Hereda todo el comportamiento de AbstractNotificacion sin agregar campos nuevos.
class Notificacion(AbstractNotificacion):
    pass

    class Meta(AbstractNotificacion.Meta):
        abstract = False
