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

        qs = plantaArbol.objects.filter(registro_salud__isnull=True)

        if self.instance and self.instance.pk and self.instance.planta_id:
            qs = qs | plantaArbol.objects.filter(pk=self.instance.planta_id)

        self.fields['planta'].queryset = qs.order_by('nombre_comun')

    def clean(self):
        cleaned = super().clean()
        planta = cleaned.get('planta')
        if not planta:
            return cleaned

        if not self.instance or not self.instance.pk:
            # Crear
            if SaludRegistro.objects.filter(planta=planta).exists():
                self.add_error('planta', 'Esta planta ya tiene un registro de salud.')
        else:
            # Editar
            if (planta.pk != self.instance.planta_id and
                SaludRegistro.objects.filter(planta=planta).exists()):
                self.add_error('planta', 'La planta seleccionada ya tiene un registro de salud.')

        return cleaned
