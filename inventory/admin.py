from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Suppliers, ProductType, Producto, HistorialMovimiento

# Registrar todos los modelos del inventario
admin.site.register(Suppliers)
admin.site.register(ProductType)
admin.site.register(Producto)

@admin.register(HistorialMovimiento)
class HistorialMovimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'tipo_producto', 'fecha', 'cambio_stock', 'stock_final', 'motivo', 'usuario')
    list_filter = ('tipo_producto', 'motivo', 'usuario')
    search_fields = ('nombre_producto', 'codigo_barras', 'motivo', 'usuario__username')
    ordering = ('-fecha',)
    # Asegúrate de que 'fecha' NO esté en readonly_fields
    # readonly_fields = ()