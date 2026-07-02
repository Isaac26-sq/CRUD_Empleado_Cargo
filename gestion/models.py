from django.db import models


class Cargo(models.Model):
    """Un cargo o puesto de trabajo. Un Cargo puede tener varios Empleados."""
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        # Facilita la visualización en el admin, el shell y los desplegables.
        return self.nombre


class Empleado(models.Model):
    """Un empleado. Cada Empleado pertenece a un único Cargo (ForeignKey)."""
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField()
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ingreso = models.DateField()
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.PROTECT,   # No permite borrar un cargo que tenga empleados asociados.
        related_name='empleados'    # Permite navegar hacia atrás: cargo.empleados.all()
    )

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
