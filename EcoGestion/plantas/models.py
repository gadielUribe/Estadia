from django.db import models

# Create your models here.

# Modelo para plantas y árboles
class plantaArbol(models.Model):
    id_planta = models.AutoField(primary_key=True)
    nombre_comun = models.CharField(verbose_name="Nombre Comun", max_length=50, null=False)
    nombre_cientifico = models.CharField(verbose_name="Nombre Científico", max_length=100, null=False)
    descripcion = models.CharField(verbose_name="Descripción", max_length=600, null=False)
    fecha_plantacion = models.DateField(verbose_name="Fecha Plantación", null=True)
    imagen_url= models.ImageField(upload_to='plantas/%Y/%m/', verbose_name="Imagen", blank=True, null=True)
    # Periodicidades como texto (p. ej. "7", "15", "mensual")
    periodicidad_riego = models.CharField(verbose_name="Periodicidad Riego", max_length=40, null=False)
    periodicidad_poda = models.CharField(verbose_name="Periodicidad Poda", max_length=40, null=False)
    periodicidad_fumigacion = models.CharField(verbose_name="Periodicidad Fumigación", max_length=40, null=False)
    lat = models.FloatField(verbose_name="Latitud", null=True)
    lng = models.FloatField(verbose_name="Longitud", null=True)

    # Información de la tabla
    class Meta:
        db_table = 'PlantaArbol'

    # Representación en cadena del objetoz
    def _str_(self):
        texto = "{0} - {1}"
        return texto.format(self.id_planta, self.nombre_cientifico)





    
