from django import forms
from django.utils import timezone

from .models import EventoAmbiental
from usuario.models import Usuario

FMT = '%Y-%m-%dT%H:%M'


class EventoForm(forms.ModelForm):
    class Meta:
        model = EventoAmbiental
        fields = ["titulo", "descripcion", "fecha_inicio", "fecha_fin", "organizador"]
        widgets = {
            "fecha_inicio": forms.DateTimeInput(attrs={"type": "datetime-local"}, format=FMT),
            "fecha_fin": forms.DateTimeInput(attrs={"type": "datetime-local"}, format=FMT),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["organizador"].queryset = Usuario.objects.all().order_by("nombre_completo")
        for name, field in self.fields.items():
            if field.required:
                field.widget.attrs.setdefault("required", "required")
                field.widget.attrs.setdefault(
                    "data-required-msg", f"El campo {field.label.lower()} es obligatorio."
                )

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get("fecha_inicio")
        fin = cleaned.get("fecha_fin")
        if inicio and fin and fin < inicio:
            self.add_error("fecha_fin", "La fecha de fin debe ser posterior a la fecha de inicio.")
        return cleaned

    def clean_fecha_inicio(self):
        fecha = self.cleaned_data.get("fecha_inicio")
        if fecha and fecha < timezone.now() - timezone.timedelta(days=1):
            raise forms.ValidationError("La fecha de inicio no puede estar demasiado en el pasado.")
        return fecha
