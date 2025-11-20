from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Usuario

SENTINELA = "********"


class LoginForm(forms.Form):
    matricula = forms.CharField(
        label="Matr�cula",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingresa tu matr�cula",
                "required": "required",
                "data-required-msg": "La matr�cula es obligatoria.",
            }
        ),
    )
    password = forms.CharField(
        label="Contrase�a",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Ingresa la contrase�a",
                "required": "required",
                "data-required-msg": "La contrase�a es obligatoria.",
            }
        ),
    )


class ValidatedPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if not Usuario.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("Correo no v�lido.")
        return email


class UsuarioForm(forms.ModelForm):
    contrasena = forms.CharField(
        label="Contrase�a",
        widget=forms.PasswordInput(
            render_value=True,
            attrs={
                "placeholder": "Deja '********' para mantener la actual",
                "data-required-msg": "La contrase�a es obligatoria.",
                "minlength": "8",
                "data-minlength-msg": "La contrase�a debe tener al menos 8 caracteres.",
            },
        ),
        required=False,
        help_text=(
            "Debe tener al menos 8 caracteres, incluir letra y n�mero, y cumplir las "
            "pol�ticas de seguridad."
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
                    "data-required-msg": "La matr�cula es obligatoria.",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "correo@ejemplo.com",
                    "required": "required",
                    "data-required-msg": "El correo electr�nico es obligatorio.",
                }
            ),
            "nombre_completo": forms.TextInput(attrs={"placeholder": "Nombre completo"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial.setdefault("contrasena", SENTINELA)
        for name, field in self.fields.items():
            if field.required:
                field.widget.attrs.setdefault("required", "required")
                field.widget.attrs.setdefault(
                    "data-required-msg", f"El campo {field.label} es obligatorio."
                )

    def clean_contrasena(self):
        data = (self.cleaned_data.get("contrasena") or "").strip()
        if not self.instance.pk and not data:
            raise forms.ValidationError("La contrase�a es obligatoria para nuevos usuarios.")

        if self.instance.pk and (data == SENTINELA or data == ""):
            return None

        if len(data) < 8:
            raise forms.ValidationError("La contrase�a debe tener al menos 8 caracteres.")
        if not any(c.isalpha() for c in data) or not any(c.isdigit() for c in data):
            raise forms.ValidationError(
                "La contrase�a debe incluir al menos una letra y un n�mero."
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
