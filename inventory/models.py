from django.db import models, connection
from django.utils.timezone import now  


class Producto(models.Model):
    name = models.CharField(max_length=200, default='Sin nombre')
    type = models.CharField(max_length=200, blank=False)
    price = models.IntegerField()
    stock = models.IntegerField(default=0)
    choices = (
        ('AVAILABLE', 'Item ready to be purchased'),
        ('SOLD', 'Item already purchased'),
        ('RESTOCKING', 'Item restocking in a few days')
    )

    status = models.CharField(max_length=10, choices=choices, default='SOLD')
    issues = models.CharField(max_length=50, default="No Issues")
    date_added = models.DateTimeField(default=now, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return 'type: {0} price: {1} date_added: {2}'.format(self.type, self.price, self.date_added)

    @classmethod
    def table_exists(cls):
        """Checks if the table for the model exists in the database."""
        return cls._meta.db_table in connection.introspection.table_names()
    
class Sellantes(Producto):
    pass

class Herramientas(Producto):
    pass

class Pinturas(Producto):
    pass

class HistorialMovimiento(models.Model):
    producto_id = models.IntegerField()
    nombre_producto = models.CharField(max_length=200)
    tipo_producto = models.CharField(max_length=50)  # "Sellante", "Herramienta", "Pintura"
    fecha = models.DateTimeField(auto_now_add=True)
    cambio_stock = models.IntegerField()  # Positivo para entrada, negativo para salida
    stock_final = models.IntegerField()
    motivo = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.nombre_producto} ({self.tipo_producto}) - {self.cambio_stock} unidades"



