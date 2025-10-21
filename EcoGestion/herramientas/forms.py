from django import forms
from .models import Herramienta, AsignacionHerramienta


class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la herramienta'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción'}),
        }


class AsignacionHerramientaForm(forms.ModelForm):
    class Meta:
        model = AsignacionHerramienta
        fields = ['herramienta', 'tarea_id', 'tarea_descripcion']
        widgets = {
            'herramienta': forms.Select(attrs={'class': 'form-select'}),
            'tarea_id': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'tarea_descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción breve de la tarea'}),
        }

