from django import forms
from .models import Suppliers, Producto, ProductType
from django.core.exceptions import ValidationError
import re


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
        # CRITICAL: Only show existing active product types - NO creation allowed
        self.fields['product_type'].queryset = ProductType.objects.filter(is_active=True)
        self.fields['product_type'].empty_label = "-- Seleccione un tipo --"
        
        # Make sure the field cannot create new objects
        self.fields['product_type'].widget.can_add_related = False
        self.fields['product_type'].widget.can_change_related = False
        self.fields['product_type'].widget.can_delete_related = False

    def clean_product_type(self):
        product_type = self.cleaned_data.get('product_type')
        if not product_type:
            raise ValidationError('Debe seleccionar un tipo de producto válido.')
        
        # Ensure the product type exists and is active
        if not ProductType.objects.filter(id=product_type.id, is_active=True).exists():
            raise ValidationError('El tipo de producto seleccionado no es válido.')
        
        return product_type

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

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Suppliers
        fields = ['empresa', 'encargado', 'email', 'numero', 'direccion']
        labels = {
            'empresa': 'Empresa',
            'encargado': 'Encargado',
            'email': 'Email',
            'numero': 'Teléfono',
            'direccion': 'Dirección'
        }
        widgets = {
            'empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la empresa'
            }),
            'encargado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del encargado'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '9 8765 4321'  # Show example without +56
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa del proveedor'
            })
        }

    def clean_empresa(self):
        empresa = self.cleaned_data.get('empresa')
        if empresa:
            empresa = empresa.strip()
            if len(empresa) < 2:
                raise ValidationError('El nombre de la empresa debe tener al menos 2 caracteres.')
            if not re.match(r'^[a-zA-Z0-9\s\.\-]+$', empresa):
                raise ValidationError('El nombre de la empresa solo puede contener letras, números, espacios, puntos y guiones.')
        return empresa

    def clean_encargado(self):
        encargado = self.cleaned_data.get('encargado')
        if encargado:
            encargado = encargado.strip()
            if len(encargado) < 2:
                raise ValidationError('El nombre del encargado debe tener al menos 2 caracteres.')
            if not re.match(r'^[a-zA-Z\s\.\-]+$', encargado):
                raise ValidationError('El nombre del encargado solo puede contener letras, espacios, puntos y guiones.')
        return encargado

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            # Check if email already exists (excluding current instance in update)
            if self.instance.pk:
                if Suppliers.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                    raise ValidationError('Ya existe un proveedor con este email.')
            else:
                if Suppliers.objects.filter(email=email).exists():
                    raise ValidationError('Ya existe un proveedor con este email.')
        return email

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if numero:
            # Remove spaces and common separators
            numero = re.sub(r'[\s\-\(\)]', '', numero)
            
            # Always add +56 prefix
            if not numero.startswith('+56'):
                numero = '+56' + numero
            
            # Validate final format
            if not re.match(r'^\+56\d{9}$', numero):
                raise ValidationError('Formato de teléfono inválido. Ingrese 9 dígitos (ej: 987654321)')
        return numero

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if direccion:
            direccion = direccion.strip()
            if len(direccion) < 10:
                raise ValidationError('La dirección debe tener al menos 10 caracteres.')
            if len(direccion) > 500:
                raise ValidationError('La dirección no puede exceder 500 caracteres.')
        return direccion

class ExcelUploadForm(forms.Form):
    file = forms.FileField(label="Archivo Excel")

