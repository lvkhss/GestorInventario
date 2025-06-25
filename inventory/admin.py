from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Suppliers, ProductType, Producto, HistorialMovimiento

# Register new dynamic models
@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Producto)
class ProductoAdmin(ImportExportModelAdmin):
    list_display = ('name', 'product_type', 'price', 'stock', 'date_added')
    list_filter = ('product_type', 'date_added')
    search_fields = ('name', 'codigo_barras')
    exclude = ('id',)

admin.site.register(Suppliers)
admin.site.register(HistorialMovimiento)