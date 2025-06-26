from django.db import models, connection
from django.utils.timezone import now  
from django.contrib.auth.models import User


class Suppliers(models.Model):
    rut = models.CharField(max_length=12, unique=True)  # Change from FloatField/DecimalField to CharField
    empresa = models.CharField(max_length=100)
    encargado = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    numero = models.CharField(max_length=15)
    direccion = models.TextField()
    
    def __str__(self):
        return self.empresa


class ProductType(models.Model):
    """Model to define product types dynamically"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo de Producto"
        verbose_name_plural = "Tipos de Productos"


class Producto(models.Model):
    name = models.CharField(max_length=200, default='Sin nombre')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, verbose_name="Tipo")
    price = models.IntegerField()
    stock = models.IntegerField(default=0)
    codigo_barras = models.CharField(max_length=50, null=True, blank=True)
    date_added = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f'{self.name} - {self.product_type.name} - ${self.price}'

    @property
    def type(self):
        """Backward compatibility property"""
        return self.product_type.name

    @classmethod
    def table_exists(cls):
        """Checks if the table for the model exists in the database."""
        return cls._meta.db_table in connection.introspection.table_names()

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

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
    precio = models.IntegerField()  # Assuming you want to track the price in the history

    def __str__(self):
        return f"{self.nombre_producto} ({self.tipo_producto}) - {self.cambio_stock} unidades"