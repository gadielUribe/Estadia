from django import forms
from .models import Producto, AsignacionProducto, Existencia


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'fecha_llegada']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_llegada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


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
