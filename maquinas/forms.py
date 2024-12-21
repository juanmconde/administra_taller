from django import forms
from .models import Cliente, Maquina, Reparacion

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'email']

class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ['cliente', 'marca', 'modelo', 'descripcion']

class ReparacionForm(forms.ModelForm):
    class Meta:
        model = Reparacion
        fields = ['maquina', 'problema_reportado', 'solucion', 'costo']
