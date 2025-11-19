from django import forms
from plantas.models import plantaArbol
from .models import SaludRegistro

class SaludForm(forms.ModelForm):
    class Meta:
        model = SaludRegistro
        fields = ['planta','estado_salud','observaciones']
        widgets = {'observaciones': forms.Textarea(attrs={'rows':3, 'class':'form-control'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['planta'].queryset = plantaArbol.objects.filter(registro_salud__isnull=False)