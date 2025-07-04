from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Suppliers, ProductType, Producto, HistorialMovimiento, CartSale, CartSaleItem
# Admin for CartSale and CartSaleItem
@admin.register(CartSale)
class CartSaleAdmin(admin.ModelAdmin):
    list_display = ('cart_code', 'user', 'created_at')
    search_fields = ('cart_code', 'user__username')
    list_filter = ('user', 'created_at')

@admin.register(CartSaleItem)
class CartSaleItemAdmin(admin.ModelAdmin):
    list_display = ('cart_sale', 'producto', 'quantity', 'price_at_sale')
    search_fields = ('cart_sale__cart_code', 'producto__name')
    list_filter = ('cart_sale', 'producto')

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