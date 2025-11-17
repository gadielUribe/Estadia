from __future__ import annotations

from django import forms
from django.contrib.auth import get_user_model

from voluntarios.models import Voluntario, AsignacionVoluntario

from .models import TareaMantenimiento


class TareaForm(forms.ModelForm):
    responsable_selector = forms.ChoiceField(required=False, label="Responsable", choices=[])
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
        self.fields["usuario_responsable"].widget = forms.HiddenInput()
        self._responsable_map = {}
        internos = []
        for user in self.fields["usuario_responsable"].queryset.order_by("nombre_completo"):
            key = f"u-{user.pk}"
            internos.append((key, user.nombre_completo))
            self._responsable_map[key] = ("user", user)
        voluntarios = []
        for vol in Voluntario.objects.all().order_by("apellido", "nombre"):
            nombre = f"{vol.nombre} {vol.apellido}".strip()
            key = f"v-{vol.pk}"
            voluntarios.append((key, nombre))
            self._responsable_map[key] = ("vol", vol)
        choices = [("", "---------")]
        if internos:
            choices.append(("Equipo interno", internos))
        if voluntarios:
            choices.append(("Voluntarios", voluntarios))
        self.fields["responsable_selector"].choices = choices
        initial = None
        if self.instance and self.instance.pk:
            if self.instance.usuario_responsable_id:
                initial = f"u-{self.instance.usuario_responsable_id}"
            else:
                asignacion = (
                    AsignacionVoluntario.objects.select_related("voluntario")
                    .filter(tarea_id=self.instance.pk)
                    .order_by("-fecha_asignacion")
                    .first()
                )
                if asignacion:
                    initial = f"v-{asignacion.voluntario_id}"
        if initial:
            self.fields["responsable_selector"].initial = initial
        self.fields["herramienta"].required = False
        self.fields["producto"].required = False

    def get_responsable(self):
        value = self.cleaned_data.get("responsable_selector")
        if not value:
            return None, None
        tipo, obj = self._responsable_map.get(value, (None, None))
        if tipo == "user":
            return obj, None
        if tipo == "vol":
            return None, obj
        return None, None
