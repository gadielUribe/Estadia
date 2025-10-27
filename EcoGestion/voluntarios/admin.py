from django.contrib import admin
from .models import Voluntario, AsignacionVoluntario


@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ("id_voluntario", "apellido", "nombre", "email", "telefono", "tipo_participacion", "fecha_registro")
    search_fields = ("nombre", "apellido", "email")
    list_filter = ("tipo_participacion",)


@admin.register(AsignacionVoluntario)
class AsignacionVoluntarioAdmin(admin.ModelAdmin):
    list_display = ("id_asignacion", "voluntario", "tarea_id", "actividad", "evento_id", "fecha_asignacion", "asignado_por")
    list_filter = ("fecha_asignacion",)
    search_fields = ("voluntario__nombre", "voluntario__apellido", "actividad", "evento_nombre")

