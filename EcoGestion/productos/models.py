from django.db import models
from django.conf import settings


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    fecha_llegada = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'Producto'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    @property
    def existencias_actuales(self) -> int:
        try:
            return self.existencia.cantidad
        except Existencia.DoesNotExist:
            return 0


class Existencia(models.Model):
    id_existencia = models.AutoField(primary_key=True)
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, db_column='id_producto', related_name='existencia')
    cantidad = models.IntegerField(default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Existencia'


class AsignacionProducto(models.Model):
    id_asignacion = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='asignaciones')
    tarea_id = models.PositiveIntegerField(help_text="ID de la tarea de mantenimiento")
    cantidad = models.PositiveIntegerField(default=1)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    asignado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'AsignacionProducto'
        ordering = ['-fecha_asignacion']

    def __str__(self):
        return f"{self.producto} x{self.cantidad} -> Tarea {self.tarea_id}"
