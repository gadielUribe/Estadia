from django.db import models
from django.conf import settings


class Herramienta(models.Model):
    ESTADO_DISPONIBLE = "disponible"
    ESTADO_EN_USO = "en_uso"
    ESTADO_MANTENIMIENTO = "mantenimiento"

    ESTADOS = (
        (ESTADO_DISPONIBLE, "Disponible"),
        (ESTADO_EN_USO, "En uso"),
        (ESTADO_MANTENIMIENTO, "Mantenimiento"),
    )

    id_herramienta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=ESTADO_DISPONIBLE,
        verbose_name="Estado"
    )

    class Meta:
        db_table = 'Herramienta'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class AsignacionHerramienta(models.Model):
    id_asignacion = models.AutoField(primary_key=True)
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE, related_name='asignaciones')
    # Mientras no exista un modelo de Tarea de Mantenimiento, almacenamos el id externo
    tarea_id = models.PositiveIntegerField(help_text="ID de la tarea de mantenimiento")
    tarea_descripcion = models.CharField(max_length=255, blank=True, help_text="Descripción breve de la tarea")
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    asignado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'AsignacionHerramienta'
        ordering = ['-fecha_asignacion']

    def __str__(self):
        return f"{self.herramienta} -> Tarea {self.tarea_id}"

