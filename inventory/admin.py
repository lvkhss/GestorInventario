from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Suppliers, ProductType, Producto, HistorialMovimiento

# Registrar todos los modelos del inventario
admin.site.register(Suppliers)
admin.site.register(ProductType)
admin.site.register(Producto)
admin.site.register(HistorialMovimiento)