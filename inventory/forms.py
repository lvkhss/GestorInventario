from django import forms
from .models import Suppliers, ProductType, Producto

class ProductoForm(forms.ModelForm):
    """Dynamic form for the new unified Producto model"""
    class Meta:
        model = Producto
        fields = ['name', 'product_type', 'price', 'stock', 'codigo_barras']
        labels = {
            'name': 'Nombre',
            'product_type': 'Tipo',
            'price': 'Precio',
            'stock': 'Stock',
            'codigo_barras': 'Código de Barras'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active product types
        self.fields['product_type'].queryset = ProductType.objects.filter(is_active=True)

class ProductTypeForm(forms.ModelForm):
    """Form for managing product types"""
    class Meta:
        model = ProductType
        fields = ['name', 'description', 'is_active']
        labels = {
            'name': 'Nombre del Tipo',
            'description': 'Descripción',
            'is_active': 'Activo'
        }

class suplierForm(forms.ModelForm):
    class Meta:
        model = Suppliers
        fields = ['empresa', 'encargado', 'email', 'numero', 'direccion']

class ExcelUploadForm(forms.Form):
    file = forms.FileField(label="Archivo Excel")

