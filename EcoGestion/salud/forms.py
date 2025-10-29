# salud/forms.py
from django import forms
from .models import SaludRegistro

class SaludForm(forms.ModelForm):
    class Meta:
        model = SaludRegistro
        fields = ['planta', 'estado_salud', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows':3, 'class':'form-control'}),
        }
