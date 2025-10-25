from django import forms
from .models import incidenciaAmbiental

class incidenciaForm(forms.ModelForm):
    class Meta:
        model = incidenciaAmbiental
        fields = [
            'titulo',
            'descripcion',
            'fecha_reporte',
            'area_campus',
            'id_planta',
            'estado',
            'id_usuario',
        ]
        widgets = {
            'fecha_reporte': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_reporte'].input_formats = ['%Y-%m-%dT%H:%M']