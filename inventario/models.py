from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    id_produ        = models.AutoField(db_column = 'idProdu', primary_key=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre
