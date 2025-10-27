from django import forms
from .models import Voluntario, AsignacionVoluntario


class VoluntarioForm(forms.ModelForm):
    class Meta:
        model = Voluntario
        fields = ['nombre', 'apellido', 'email', 'telefono', 'tipo_participacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_participacion': forms.Select(attrs={'class': 'form-select'}),
        }


class AsignacionVoluntarioForm(forms.ModelForm):
    class Meta:
        model = AsignacionVoluntario
        fields = ['voluntario', 'tarea_id', 'actividad', 'evento_id', 'evento_nombre']
        widgets = {
            'voluntario': forms.Select(attrs={'class': 'form-select'}),
            'tarea_id': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'actividad': forms.TextInput(attrs={'class': 'form-control'}),
            'evento_id': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'evento_nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

