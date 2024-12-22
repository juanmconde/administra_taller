from django import forms
from django.forms import formset_factory
from .models import Cliente, Maquina, Reparacion, DetalleReparacion

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "apellido", "telefono"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
        }

class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ["tipo", "problema", "fecha_entrada"]
        widgets = {
            "tipo": forms.TextInput(attrs={"class": "form-control"}),
            "problema": forms.Textarea(attrs={"class": "form-control"}),
            "fecha_entrada": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

class ReparacionForm(forms.ModelForm):
    class Meta:
        model = Reparacion
        fields = ['mano_obra', 'observaciones', 'fecha', 'maquina', 'total']

class DetalleReparacionForm(forms.ModelForm):
    class Meta:
        model = DetalleReparacion
        fields = ['cantidad', 'descripcion', 'precio']

DetalleReparacionFormSet = formset_factory(DetalleReparacionForm, extra=10, can_delete=True)