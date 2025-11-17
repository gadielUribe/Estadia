from django.conf import settings
from django.db import models


class EventoAmbiental(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(blank=True, null=True)
    organizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eventos_organizados",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_inicio"]
        verbose_name = "Evento ambiental"
        verbose_name_plural = "Eventos ambientales"

    def __str__(self) -> str:
        return f"{self.titulo} ({self.fecha_inicio.date()})"
