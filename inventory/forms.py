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
        fields = ['empresa', 'encargado', 'email', 'numero', 'direccion','rut']
        labels = {
            'empresa': 'Empresa',
            'encargado': 'Encargado',
            'email': 'Email',
            'numero': 'Teléfono',
            'direccion': 'Dirección',
            'rut': 'RUT'
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
                'placeholder': '9 8765 4321'  # No +56
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa del proveedor'
            }),
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '99999999-9'  
            }),
        }

    def clean_empresa(self):
        empresa = self.cleaned_data.get('empresa')
        if empresa:
            empresa = empresa.strip()
            if len(empresa) < 3:
                raise ValidationError('El nombre de la empresa debe tener al menos 3 caracteres.')
            if not re.match(r'^[a-zA-ZÀ-ÿ\s\.\-]+$', empresa):
                raise ValidationError('El nombre de la empresa solo puede contener letras, espacios, puntos y guiones.')
        return empresa

    def clean_encargado(self):
        encargado = self.cleaned_data.get('encargado')
        if encargado:
            encargado = encargado.strip()
            if len(encargado) < 2:
                raise ValidationError('El nombre del encargado debe tener al menos 2 caracteres.')
            if not re.match(r'^[a-zA-Z\s\-]+$', encargado):
                raise ValidationError('El nombre del encargado solo puede contener letras, espacios y guiones.')
        return encargado

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()

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
     
            numero = re.sub(r'[\s\-\(\)]', '', numero)
            
          
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

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            # Convert to string and clean
            rut_original = str(rut).strip().upper()
            
            # Remove dots and hyphens for validation
            rut_limpio = re.sub(r'[.\-]', '', rut_original)
            
            # Verificar longitud mínima
            if len(rut_limpio) < 2:
                raise ValidationError('El RUT debe tener al menos 2 caracteres.')
            
            # Separar cuerpo y dígito verificador
            cuerpo = rut_limpio[:-1]
            dv = rut_limpio[-1]
            
            # Validar que el cuerpo sean solo dígitos
            if not re.match(r'^\d+$', cuerpo):
                raise ValidationError('El cuerpo del RUT solo puede contener números.')
            
            # Validar longitud del cuerpo (7-8 dígitos)
            if len(cuerpo) < 7 or len(cuerpo) > 8:
                raise ValidationError('El RUT debe tener entre 7 y 8 dígitos.')
            
            # Validar que no empiece con 0
            if cuerpo.startswith('0'):
                raise ValidationError('El RUT no puede empezar con 0.')
            
            # Calcular dígito verificador esperado (Módulo 11)
            reverso = cuerpo[::-1]  # Invertir string
            multiplicador = 2
            suma = 0
            
            for digito in reverso:
                suma += int(digito) * multiplicador
                multiplicador += 1
                if multiplicador == 8:
                    multiplicador = 2
            
            dv_calculado = 11 - (suma % 11)
            
            if dv_calculado == 11:
                dv_esperado = '0'
            elif dv_calculado == 10:
                dv_esperado = 'K'
            else:
                dv_esperado = str(dv_calculado)
            
            # Comparar dígito verificador
            if dv != dv_esperado:
                raise ValidationError(f'Rut no válido.')
            
            # Formatear RUT con guión para guardar
            rut_formateado = f"{cuerpo}-{dv}"
            
            # Validar unicidad
            if self.instance.pk:
                if Suppliers.objects.exclude(pk=self.instance.pk).filter(rut=rut_formateado).exists():
                    raise ValidationError('Ya existe un proveedor con este RUT.')
            else:
                if Suppliers.objects.filter(rut=rut_formateado).exists():
                    raise ValidationError('Ya existe un proveedor con este RUT.')
        
        return rut_formateado

class ExcelUploadForm(forms.Form):
    file = forms.FileField(label="Archivo Excel")

