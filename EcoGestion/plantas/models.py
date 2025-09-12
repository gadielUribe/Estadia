from django.db import models

# Create your models here.
class plantaArbol(models.Model):
    id_planta = models.AutoField(primary_key=True)
    descripcion = models.CharField(verbose_name="Descripción", max_length=600, null=False)
    nombre_cientifico = models.CharField(verbose_name="NombreCientífico", max_length=100, null=False)
    fecha_plantacion = models.DateTimeField(verbose_name="FechaPlantación", null=True)
    imagen_url= models.CharField(verbose_name="ImagenURL", max_length=300, null=True)
    periodicidad_riego = models.IntegerField(verbose_name="PeriodicidadRiego", null=False)
    periodicidad_poda = models.IntegerField(verbose_name="PeriodicidadPoda", null=False)
    periodicidad_fumigacion = models.IntegerField(verbose_name="PeriodicidadFumigación", null=False)
    latitud = models.FloatField(verbose_name="Latitud", null=False)
    longitud = models.FloatField(verbose_name="Longitud", null=False)
    id_ubicacion = models.IntegerField(verbose_name="IDUbicación", null=False)

    class Meta:
        db_table = "PlantaArbol"
        managed = False

    def __str__(self):
        texto = "{0} - {1}"
        return texto.format(self.id, self.nombre_cientifico)



    