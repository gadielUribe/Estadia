from django.db import models
from django.conf import settings


class Voluntario(models.Model):
    TIPO_PARTICIPACION = (
        ('estudiante', 'Estudiante'),
        ('trabajador', 'Trabajador'),
        ('externo', 'Voluntario externo'),
    )

    id_voluntario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, blank=True)
    telefono = models.CharField(max_length=25, blank=True)
    tipo_participacion = models.CharField(max_length=20, choices=TIPO_PARTICIPACION, default='estudiante')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Voluntario'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


class AsignacionVoluntario(models.Model):
    id_asignacion = models.AutoField(primary_key=True)
    voluntario = models.ForeignKey(Voluntario, on_delete=models.CASCADE, related_name='asignaciones')
    tarea_id = models.PositiveIntegerField(help_text="ID de la tarea/actividad")
    actividad = models.CharField(max_length=150, blank=True, help_text="Descripción corta de la actividad")
    evento_id = models.PositiveIntegerField(null=True, blank=True, help_text="ID del evento (opcional)")
    evento_nombre = models.CharField(max_length=150, blank=True)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    asignado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'AsignacionVoluntario'
        ordering = ['-fecha_asignacion']

    def __str__(self):
        return f"{self.voluntario} -> tarea {self.tarea_id}"

