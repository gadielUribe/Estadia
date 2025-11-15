from django.db import models
from django.conf import settings

class SaludRegistro(models.Model):
    ESTADOS = [('verde','Verde'),('amarillo','Amarillo'),('rojo','Rojo')]

    id_registro = models.AutoField(primary_key=True)
    planta = models.OneToOneField(
        'plantas.plantaArbol',
        on_delete=models.CASCADE,
        related_name='registro_salud',
        verbose_name="Planta/Árbol",
        db_index=True,
    )
    fecha_actualizacion = models.DateTimeField(auto_now_add=True, db_index=True)
    estado_salud = models.CharField(max_length=8, choices=ESTADOS, default='verde', db_index=True)
    usuario = models.ForeignKey('usuario.Usuario', on_delete=models.SET_NULL, null=True, blank=True, related_name='registros_salud')
    observaciones = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'SaludRegistro'
        ordering = ['-fecha_actualizacion','-id_registro']
        indexes = [models.Index(fields=['planta','fecha_actualizacion']),
                   models.Index(fields=['estado_salud'])]

    def __str__(self):
        u = f"{self.usuario.matricula}" if self.usuario else "sistema"
        return f"[{self.fecha_actualizacion:%Y-%m-%d %H:%M}] {self.planta_id} → {self.estado_salud} @ {u}"

class SaludHistorial(models.Model):
    id_historial = models.AutoField(primary_key=True)
    planta = models.ForeignKey('plantas.plantaArbol', on_delete=models.CASCADE, related_name='historial_salud')
    usuario = models.ForeignKey('usuario.Usuario', on_delete=models.SET_NULL, null=True, blank=True)
    fecha_evento = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de actualización")
    estado_salud = models.CharField(max_length=8, choices=[
        ('verde', 'Verde'),
        ('amarillo', 'Amarillo'),
        ('rojo', 'Rojo'),
    ])
    observaciones = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'SaludHistorial'
        ordering = ['-fecha_evento', '-id_historial']

    def __str__(self):
        return f"{self.planta.nombre_comun} - {self.estado_salud} ({self.fecha_evento:%Y-%m-%d %H:%M})"