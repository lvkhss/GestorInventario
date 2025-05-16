from django.db import models, connection
from django.utils.timezone import now  # 'now' ftimezone-aware timestamps xd


class Producto(models.Model):
    type = models.CharField(max_length=200, blank=False)
    price = models.IntegerField()

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


