from django.conf import settings
from django.db import models
from django.utils import timezone


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
    usuario_responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="tareas_mantenimiento")
    modificado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="tareas_mantenimiento_modificadas")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "TareaMantenimiento"
        ordering = ["fecha_programada"]

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.planta.nombre_comun} ({self.fecha_programada.date()})"

    def marcar_realizada(self, by_user=None, observaciones: str | None = None):
        self.estado = self.ESTADO_REALIZADA
        self.fecha_realizacion = timezone.now()
        if observaciones is not None:
            self.observaciones = (self.observaciones or "").strip() + ("\n" if self.observaciones else "") + observaciones
        if by_user is not None:
            self.modificado_por = by_user
        self.save(update_fields=["estado", "fecha_realizacion", "observaciones", "modificado_por", "actualizado_en"])
