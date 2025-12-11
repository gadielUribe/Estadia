from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


# TareaMantenimiento: tareas programadas para riego, poda o fumigacion de plantas.
# Campos principales: planta, tipo de tarea, fechas, estado, recursos asociados y responsables.
class TareaMantenimiento(models.Model):
    TIPO_RIEGO = "riego"
    TIPO_PODA = "poda"
    TIPO_FUMIGACION = "fumigacion"
    TIPOS = (
        (TIPO_RIEGO, "Riego"),
        (TIPO_PODA, "Poda"),
        (TIPO_FUMIGACION, "Fumigación"),
    )

    ESTADO_PENDIENTE = "pendiente"
    ESTADO_REALIZADA = "realizada"
    ESTADOS = (
        (ESTADO_PENDIENTE, "Pendiente"),
        (ESTADO_REALIZADA, "Realizada"),
    )

    id = models.AutoField(primary_key=True)
    planta = models.ForeignKey("plantas.plantaArbol", on_delete=models.CASCADE, related_name="tareas")
    tipo = models.CharField(max_length=20, choices=TIPOS)
    fecha_programada = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_PENDIENTE)
    fecha_realizacion = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    herramienta = models.ForeignKey("herramientas.Herramienta", on_delete=models.SET_NULL, null=True, blank=True)
    producto = models.ForeignKey("productos.Producto", on_delete=models.SET_NULL, null=True, blank=True)
    usuario_responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tareas_mantenimiento",
    )
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tareas_mantenimiento_modificadas",
    )
    recordatorio_24h_enviado = models.BooleanField(default=False)
    vencimiento_notificado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "TareaMantenimiento"
        ordering = ["fecha_programada"]

    # __str__(): devuelve una descripcion corta con tipo, planta y fecha programada.
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.planta.nombre_comun} ({self.fecha_programada.date()})"

    # marcar_realizada(by_user=None, observaciones=None): marca la tarea como completada.
    # Entrada: usuario que marca y observaciones opcionales. Salida: guarda cambios en BD.
    def marcar_realizada(self, by_user=None, observaciones: str | None = None):
        self.estado = self.ESTADO_REALIZADA
        self.fecha_realizacion = timezone.now()
        if observaciones is not None:
            prefix = ("\n" if self.observaciones else "")
            self.observaciones = (self.observaciones or "").strip() + prefix + observaciones
        if by_user is not None:
            self.modificado_por = by_user
        self.save(update_fields=["estado", "fecha_realizacion", "observaciones", "modificado_por", "actualizado_en"])

    # save(*args, **kwargs): reestablece banderas de recordatorio si se reprograma la tarea pendiente.
    # Entrada: argumentos de guardado normales. Salida: persiste la tarea y banderas actualizadas.
    def save(self, *args, **kwargs):
        # Rehabilitar recordatorios/notificaciones si se reprograma mientras sigue pendiente
        try:
            if self.pk and self.estado == self.ESTADO_PENDIENTE:
                prev = TareaMantenimiento.objects.get(pk=self.pk)
                if prev.fecha_programada != self.fecha_programada:
                    now = timezone.now()
                    if self.fecha_programada and self.fecha_programada > now + timedelta(hours=24):
                        self.recordatorio_24h_enviado = False
                    self.vencimiento_notificado = False
        except TareaMantenimiento.DoesNotExist:
            pass
        super().save(*args, **kwargs)
