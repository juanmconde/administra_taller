from django.db import models
from datetime import date
import uuid

def cliente_generico():
    cliente, _ = Cliente.objects.get_or_create(
        nombre="Genérico", apellido="Genérico", telefono="0000000000"
    )
    return cliente.id

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.telefono})"

class Maquina(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="maquinas",
        default=cliente_generico,
    )
    tipo = models.CharField(max_length=100)
    problema = models.TextField()
    fecha_entrada = models.DateField(default=date.today)
    id_unico = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo} ({self.id_unico})"

class Reparacion(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name="reparaciones")
    fecha = models.DateField(default=date.today)
    mano_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reparación de {self.maquina.tipo} - {self.fecha}"

class DetalleReparacion(models.Model):
    reparacion = models.ForeignKey('Reparacion', on_delete=models.CASCADE, related_name='detalles')
    cantidad = models.PositiveIntegerField(default=1)
    descripcion = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio

