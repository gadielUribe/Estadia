from django import forms


class plantaForm(forms.Form):
    descripcion = forms.CharField(label="Descripción", max_length=600)
    nombre_cientifico = forms.CharField(label="NombreCientífico", max_length=100)
    fecha_plantacion = forms.DateTimeField(label="FechaPlantación")
    imagen_url= forms.CharField(label="ImagenURL", max_length=300)
    periodicidad_riego = forms.IntegerField(label="PeriodicidadRiego")
    periodicidad_poda = forms.IntegerField(label="PeriodicidadPoda")
    periodicidad_fumigacion = forms.IntegerField(label="PeriodicidadFumigación")
    latitud = forms.FloatField(label="Latitud")
    longitud = forms.FloatField(label="Longitud")
    id_ubicacion = forms.IntegerField(label="IDUbicación")

    