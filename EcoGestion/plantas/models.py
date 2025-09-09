from django.db import models

# Create your models here.
class plantaArbol(models.Model):
    descripcion = models.CharField(verbose_name="Descripción", max_length=600, null=False)
    nombre_cientifico = models.CharField(verbose_name="Nombre Científico", max_length=100, null=False)
    fecha_plantacion = models.DateTimeField