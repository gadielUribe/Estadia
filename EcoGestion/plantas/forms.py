from django import forms
from .models import plantaArbol

FMT = '%Y-%m-%d'

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
            'fecha_plantacion': forms.DateInput(attrs={'type': 'date'}, format=FMT),
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),
            'imagen_url': forms.FileInput(),
        }

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('lat') or not cleaned.get('lng'):
            raise forms.ValidationError("Selecciona la ubicacion")
        return cleaned


class PlantaCreateForm(forms.ModelForm):
    ESTADOS = [
        ('verde', 'Verde'),
        ('amarillo', 'Amarillo'),
        ('rojo', 'Rojo'),
    ]

    estado_salud = forms.ChoiceField(
        choices=ESTADOS,
        initial='verde',
        label="Estado de salud"
    )
    observaciones = forms.CharField(
        label="Observaciones",
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )

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
            'imagen_url': forms.FileInput(),
        }

    def clean(self):
        cleaned = super().clean()
        estado = cleaned.get('estado_salud')
        obs = (cleaned.get('observaciones') or '').strip()

        # Validar ubicación
        if not cleaned.get('lat') or not cleaned.get('lng'):
            raise forms.ValidationError("Selecciona la ubicacion")

        # Si es amarillo/rojo, observaciones obligatorias
        if estado in ('amarillo', 'rojo') and not obs:
            self.add_error('observaciones', 'Describe brevemente la situación si el estado no es verde.')
        return cleaned
