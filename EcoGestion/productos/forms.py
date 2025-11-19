from django import forms
from django.utils import timezone
from .models import Producto, AsignacionProducto, Existencia

FMT = "%Y-%m-%d"

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "fecha_llegada"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "fecha_llegada": forms.DateInput(attrs={"class": "form-control", "type": "date"}, format=FMT),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fecha_llegada"].input_formats = [FMT]

    def clean_fecha_llegada(self):
        fecha = self.cleaned_data.get("fecha_llegada")
        if not fecha:
            return fecha
        hoy = timezone.localdate()
        if fecha > hoy:
            raise forms.ValidationError("La fecha de llegada no puede ser posterior a hoy.")
        return fecha



class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Existencia
        fields = ['cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class AsignacionProductoForm(forms.ModelForm):
    class Meta:
        model = AsignacionProducto
        fields = ['producto', 'tarea_id', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'tarea_id': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean(self):
        cleaned = super().clean()
        producto = cleaned.get('producto')
        cantidad = cleaned.get('cantidad')
        stock = producto.existencia.cantidad if producto and hasattr(producto, 'existencia') else 0
        if producto and cantidad and cantidad > stock:
            raise forms.ValidationError("No hay existencias suficientes para esta asignación.")
        return cleaned
