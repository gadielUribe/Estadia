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
            'descripcion_ubicacion',
            'procedencia',
            'fecha_llegada',
            'lat',
            'lng',
        ]
        widgets = {
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),
        }

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('lat') or not cleaned.get('lng'):
            raise forms.ValidationError("Selecciona la ubicacion")
        return cleaned
     