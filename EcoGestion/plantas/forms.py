from django import forms
from .models import plantaArbol

# Formulario basado en el modelo plantaArbol
class plantaForm(forms.ModelForm):
    class Meta:
        model = plantaArbol
        fields = [
            'descripcion',
            'nombre_cientifico',
            'fecha_plantacion',
            'imagen_url',
            'periodicidad_riego',
            'periodicidad_poda',
            'periodicidad_fumigacion',
            'latitud',
            'longitud',
        ]

     