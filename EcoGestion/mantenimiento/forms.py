from __future__ import annotations

from django import forms
from django.contrib.auth import get_user_model

from .models import TareaMantenimiento


class TareaForm(forms.ModelForm):
    generar_automaticas = forms.BooleanField(
        required=False,
        label="Generar automáticamente futuras tareas según periodicidad de la planta",
    )
    horizonte_dias = forms.IntegerField(
        required=False,
        min_value=1,
        initial=60,
        label="Horizonte (días) para autogenerar",
    )

    class Meta:
        model = TareaMantenimiento
        fields = [
            "planta",
            "tipo",
            "fecha_programada",
            "usuario_responsable",
            "herramienta",
            "producto",
            "observaciones",
        ]
        widgets = {
            "fecha_programada": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        User = get_user_model()
        self.fields["usuario_responsable"].required = False
        self.fields["usuario_responsable"].queryset = User.objects.filter(rol="mantenimiento")
        self.fields["herramienta"].required = False
        self.fields["producto"].required = False
