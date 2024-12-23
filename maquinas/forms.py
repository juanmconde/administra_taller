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
        fields = ["maquina", "problema", "fecha_entrada"]
        widgets = {
            "maquina": forms.TextInput(attrs={"class": "form-control"}),
            "problema": forms.Textarea(attrs={"rows": 3, "cols": 40}),
            "fecha_entrada": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }


class DetalleReparacionForm(forms.ModelForm):
    class Meta:
        model = DetalleReparacion
        fields = ["descripcion", "cantidad", "precio"]

    def clean(self):
        cleaned_data = super().clean()
        descripcion = cleaned_data.get("descripcion")
        cantidad = cleaned_data.get("cantidad")
        precio = cleaned_data.get("precio")

        if not descripcion:
            raise forms.ValidationError("La descripción no puede estar vacía.")
        if not cantidad or cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a 0.")
        if not precio or precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")
        return cleaned_data


class DetalleReparacionForm(forms.ModelForm):
    class Meta:
        model = DetalleReparacion
        fields = ["cantidad", "descripcion", "precio"]


DetalleReparacionFormSet = formset_factory(
    DetalleReparacionForm, extra=10, can_delete=True
)

class ReparacionForm(forms.ModelForm):
    class Meta:
        model = Reparacion
        fields = ["maquina", "fecha", "mano_obra", "observaciones"]

    def __init__(self, *args, **kwargs):
        cliente = kwargs.pop("cliente", None)  # Extrae el argumento cliente
        super().__init__(*args, **kwargs)
        if cliente:
            # Filtra las máquinas disponibles según el cliente
            self.fields["maquina"].queryset = cliente.maquinas.all()