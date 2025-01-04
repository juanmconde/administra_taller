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
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('reparada', 'Reparada'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="maquinas",
        default=cliente_generico,
    )
    maquina = models.CharField(max_length=100)
    problema = models.TextField()
    fecha_entrada = models.DateField(default=date.today)
    id_unico = models.CharField(max_length=255, unique=True, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')  # Nuevo campo

    def __str__(self):
        return f"{self.maquina} ({self.fecha_entrada})"

    def problema_corto(self):
        return self.problema[:50] + "..." if len(self.problema) > 50 else self.problema


class Reparacion(models.Model):
    id_unico = models.CharField(max_length=20, unique=True, blank=True, null=True) # Nuevo
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today)
    mano_obra = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField()
    # Si tienes más campos, agrégalos aquí
    def save(self, *args, **kwargs):
        if not self.id_unico:
            ultimo_id = Reparacion.objects.count() + 1
            self.id_unico = f"REP-{date.today().strftime('%Y%m%d')}-{ultimo_id:04d}"
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.id_unico} - {self.maquina} ({self.cliente})" # Esto es nuevo
        # return f"Reparación de {self.maquina.maquina} - {self.fecha}"  # pylint: disable=no-member

class DetalleReparacion(models.Model):
    reparacion = models.ForeignKey('Reparacion', on_delete=models.CASCADE, related_name='detalles')
    cantidad = models.PositiveIntegerField(default=1)
    descripcion = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=1)

    def subtotal(self):
        return self.cantidad * self.precio

