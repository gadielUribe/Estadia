from __future__ import annotations

from django import forms
from django.contrib.auth import get_user_model

from .models import TareaMantenimiento


class TareaForm(forms.ModelForm):
    repetir = forms.BooleanField(
        required=False,
        label="Programar repetición automática",
        help_text="Si se marca, se crearán más tareas con la misma información.",
    )
    cada_dias = forms.IntegerField(
        required=False,
        min_value=1,
        label="Cada cuántos días",
        help_text="Intervalo entre cada tarea generada",
    )
    repeticiones = forms.IntegerField(
        required=False,
        min_value=1,
        initial=3,
        label="Cuántas veces generar",
        help_text="Número de tareas adicionales a crear",
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
