from django.db import models, connection
from django.utils.timezone import now  
from django.contrib.auth.models import User



class Suppliers(models.Model):
    empresa = models.CharField(max_length=100)
    encargado = models.CharField(max_length=100)
    email = models.EmailField()
    numero = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.empresa} - {self.encargado}"

class Producto(models.Model):
    name = models.CharField(max_length=200, default='Sin nombre')
    type = models.CharField(max_length=200, blank=False)
    price = models.IntegerField()
    stock = models.IntegerField(default=0)
    codigo_barras = models.CharField(max_length=50, null=True, blank=True)
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


class ProductoReal(Producto):
    pass
    
class Sellantes(Producto):
    pass

class Herramientas(Producto):
    pass

class Pinturas(Producto):
    pass

class HistorialMovimiento(models.Model):
    producto_id = models.IntegerField()
    nombre_producto = models.CharField(max_length=200)
    tipo_producto = models.CharField(max_length=50)
    codigo_barras = models.CharField(max_length=100, blank=True, null=True) 
    fecha = models.DateTimeField(auto_now_add=True)
    cambio_stock = models.IntegerField()
    stock_final = models.IntegerField()
    motivo = models.CharField(max_length=255, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_producto} ({self.tipo_producto}) - {self.cambio_stock} unidades"