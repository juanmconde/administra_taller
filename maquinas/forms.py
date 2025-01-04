from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from .models import Cliente, Maquina, Reparacion, DetalleReparacion
from datetime import date


# Inline formset para DetalleReparacion
DetalleReparacionFormSet = inlineformset_factory(
    Reparacion,
    DetalleReparacion,
    fields=["cantidad", "descripcion", "precio"],
    extra=1,
    can_delete=True,
)

# Formulario para Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "apellido", "telefono"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
        }

# Formulario para Maquina
class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ["maquina", "problema", "fecha_entrada"]
        widgets = {
            "maquina": forms.TextInput(attrs={"class": "form-control"}),
            "problema": forms.Textarea(attrs={"rows": 3, "cols": 40}),
            "fecha_entrada": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer la fecha actual si no hay valor inicial
        if not self.initial.get('fecha_entrada'):
            self.fields['fecha_entrada'].initial = date.today()


# Formulario para DetalleReparacion
class DetalleReparacionForm(forms.ModelForm):
    class Meta:
        model = DetalleReparacion
        fields = ["cantidad", "descripcion", "precio"]
        widgets = {
            "descripcion": forms.TextInput(attrs={"placeholder": "Escribe la descripción..."}),  # Placeholder
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get("descripcion", "").strip()
        if not descripcion:  # Validación personalizada para evitar descripciones vacías
            raise forms.ValidationError("La descripción no puede estar vacía.")
        return descripcion

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get("cantidad")
        precio = cleaned_data.get("precio")

        if not cantidad or cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a 0.")
        if not precio or precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")
        return cleaned_data


# Formulario para Reparacion
class ReparacionForm(forms.ModelForm):
    class Meta:
        model = Reparacion
        fields = ["maquina", "fecha", "mano_obra", "observaciones"]
        widgets = {
            "maquina": forms.Select(attrs={"class": "form-control"}),
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "mano_obra": forms.NumberInput(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        cliente = kwargs.pop("cliente", None)  # Extrae el argumento cliente
        super().__init__(*args, **kwargs)
        if cliente:
            self.fields["maquina"].queryset = Maquina.objects.filter(cliente=cliente)
