from django.contrib import admin
from .models import Producto, AsignacionProducto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id_producto", "nombre", "fecha_llegada")
    search_fields = ("nombre",)


@admin.register(AsignacionProducto)
class AsignacionProductoAdmin(admin.ModelAdmin):
    list_display = ("id_asignacion", "producto", "cantidad", "tarea_id", "fecha_asignacion", "asignado_por")
    list_filter = ("fecha_asignacion",)
    search_fields = ("producto__nombre",)
