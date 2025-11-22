from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Usuario

SENTINELA = "********"


class LoginForm(forms.Form):
    matricula = forms.CharField(
        label="Matrícula",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingresa tu matrícula",
                "required": "required",
                "data-required-msg": "La matrícula es obligatoria.",
            }
        ),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Ingresa la contraseña",
                "required": "required",
                "data-required-msg": "La contraseña es obligatoria.",
            }
        ),
    )


class ValidatedPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if not Usuario.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("Correo no válido.")
        return email


class UsuarioForm(forms.ModelForm):
    contrasena = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            render_value=True,
            attrs={
                "placeholder": "Ingresa la contraseña",
                "data-required-msg": "La contraseña es obligatoria.",
                "minlength": "8",
                "data-minlength-msg": "La contraseña debe tener al menos 8 caracteres.",
            },
        ),
        required=False,
        help_text=(
            "Debe tener al menos 8 caracteres, incluir letra y número, y cumplir las "
            "políticas de seguridad."
        ),
    )

    class Meta:
        model = Usuario
        fields = ["matricula", "email", "nombre_completo", "rol"]
        widgets = {
            "matricula": forms.TextInput(
                attrs={
                    "placeholder": "Ej. ABC1234",
                    "required": "required",
                    "data-required-msg": "La matrícula es obligatoria.",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "correo@ejemplo.com",
                    "required": "required",
                    "data-required-msg": "El correo electrónico es obligatorio.",
                }
            ),
            "nombre_completo": forms.TextInput(attrs={"placeholder": "Nombre completo"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        es_edicion = bool(self.instance and self.instance.pk)

        if es_edicion:
            self.initial.setdefault("contrasena", SENTINELA)
            self.fields["contrasena"].widget.attrs["placeholder"] = (
                f"Deja '{SENTINELA}' para mantener la actual"
            )
        else:
            # En creación, limpiar cualquier valor inicial y usar placeholder genérico
            self.initial.pop("contrasena", None)
            self.fields["contrasena"].widget.attrs["placeholder"] = "Ingresa la contraseña"

        for name, field in self.fields.items():
            if field.required:
                field.widget.attrs.setdefault("required", "required")
                field.widget.attrs.setdefault(
                    "data-required-msg", f"El campo {field.label} es obligatorio."
                )

    def clean_contrasena(self):
        data = (self.cleaned_data.get("contrasena") or "").strip()
        if not self.instance.pk and not data:
            raise forms.ValidationError("La contraseña es obligatoria para nuevos usuarios.")

        if self.instance.pk and (data == SENTINELA or data == ""):
            return None

        if len(data) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not any(c.isalpha() for c in data) or not any(c.isdigit() for c in data):
            raise forms.ValidationError(
                "La contraseña debe incluir al menos una letra y un número."
            )

        try:
            validate_password(data, self.instance or Usuario())
        except ValidationError as exc:
            raise forms.ValidationError(exc.messages)

        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("contrasena")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
