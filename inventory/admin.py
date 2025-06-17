from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Sellantes, Herramientas, Pinturas, Suppliers, ProductoReal
from .models import HistorialMovimiento
# Register your models here.

# admin.site.register(item)
@admin.register(Sellantes, Herramientas, Pinturas)
class ViewAdmin(ImportExportModelAdmin):
    exclude = ('id', )
admin.site.register(Suppliers)
admin.site.register(ProductoReal)
admin.site.register(HistorialMovimiento)