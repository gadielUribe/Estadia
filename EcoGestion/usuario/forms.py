from django import forms
from django.contrib.auth.forms import PasswordResetForm

from .models import Usuario


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
            attrs={
                "placeholder": "Ingresa una contraseña",
                "data-required-msg": "La contraseña es obligatoria.",
            }
        ),
        required=False,
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
        for name, field in self.fields.items():
            if field.required:
                field.widget.attrs.setdefault("required", "required")
                field.widget.attrs.setdefault(
                    "data-required-msg", f"El campo {field.label} es obligatorio."
                )

    def clean_contrasena(self):
        data = self.cleaned_data.get("contrasena")
        if not self.instance.pk and not data:
            raise forms.ValidationError("La contraseña es obligatoria para nuevos usuarios.")
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("contrasena")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
