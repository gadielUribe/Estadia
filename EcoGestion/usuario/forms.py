from django import forms
from .models import Usuario

class LoginForm(forms.Form):
    matricula = forms.CharField(label="Matrícula")
    password = forms.CharField(widget=forms.PasswordInput)

class UsuarioForm(forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Usuario
        fields = ['matricula', 'email', 'nombre_completo', 'contraseña', 'rol']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['contraseña']:
            user.set_password(self.cleaned_data['contraseña'])
        if commit:
            user.save()
        return user