from django import forms
from .models import plantaArbol


class plantaForm(forms.ModelForm):
    class Meta:
        model = plantaArbol
        fields = [
            'nombre_comun',
            'nombre_cientifico',
            'descripcion',
            'fecha_plantacion',
            'imagen_url',
            'periodicidad_riego',
            'periodicidad_poda',
            'periodicidad_fumigacion',
            'lat',
            'lng',
        ]
        widgets = {
            'fecha_plantacion': forms.DateInput(attrs={'type': 'date'}),
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),
        }

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('lat') or not cleaned.get('lng'):
            raise forms.ValidationError("Selecciona la ubicacion")
        return cleaned
     