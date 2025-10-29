from django.db import models

class incidenciaAmbiental(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('resuelto', 'Resuelto'),
    ]

    id_incidencia = models.AutoField(primary_key=True)
    titulo = models.CharField(verbose_name="Título", max_length=150, null=False)
    descripcion = models.CharField(verbose_name="Descripción", max_length=600, null=False)
    fecha_reporte = models.DateTimeField(verbose_name="FechaReporte", null=False)
    area_campus = models.CharField(verbose_name="ÁreaCampus", max_length=100, null=False)
    id_planta = models.ForeignKey('plantas.plantaArbol', on_delete=models.CASCADE, verbose_name="IDÁrbol", null=True)
    estado = models.CharField(verbose_name="Estado", choices=ESTADOS, default='pendiente', max_length=40)
    id_usuario = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE, verbose_name="IDUsuario", null=True)

    class Meta:
        db_table = 'IncidenciaAmbiental'

    # Representación en cadena del objetoz
    def __str__(self):
        texto = "{0} - {1}"
        return texto.format(self.id_incidencia, self.titulo)