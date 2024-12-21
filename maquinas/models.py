from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Maquina(models.Model):
    cliente = models.ForeignKey(Cliente, related_name="maquinas", on_delete=models.CASCADE)
    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.cliente.nombre})"

class Reparacion(models.Model):
    maquina = models.ForeignKey(Maquina, related_name="reparaciones", on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(auto_now_add=True)
    problema_reportado = models.TextField()
    solucion = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Reparación {self.id} ({self.maquina})"
