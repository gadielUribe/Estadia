from django.contrib import admin
from .models import Herramienta, AsignacionHerramienta


@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ("id_herramienta", "nombre")
    search_fields = ("nombre",)


@admin.register(AsignacionHerramienta)
class AsignacionHerramientaAdmin(admin.ModelAdmin):
    list_display = ("id_asignacion", "herramienta", "tarea_id", "fecha_asignacion", "asignado_por")
    list_filter = ("fecha_asignacion",)
    search_fields = ("herramienta__nombre", "tarea_descripcion")

