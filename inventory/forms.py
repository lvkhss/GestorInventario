from django import forms
from .models import *
from .models import Suppliers

TIPOS_PRODUCTO = (
    ('Sellantes', 'Sellante'),
    ('Herramientas', 'Herramienta'),
    ('Pinturas', 'Pintura'),
)

class ProductoForm(forms.Form):
    name = forms.CharField(label="Nombre", max_length=200)
    codigo_barras =forms.CharField(label="Codigo Barras")
    price = forms.IntegerField(label="Precio")
    type = forms.ChoiceField(label="Tipo", choices=TIPOS_PRODUCTO)
    date_added = forms.DateTimeField(label='Fecha de ingreso', initial=now, required=False, disabled=True,)

class SellanteForm(forms.ModelForm):
    class Meta:
        model = Sellantes
        fields = ['name', 'price', 'type', 'stock', 'codigo_barras']
        labels = {
            'name': 'Nombre',
            'type': 'Tipo',
            'price': 'Precio',
            'stock': 'Stock',
            'codigo_barras':'Codigo Barras'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_added'] = forms.DateTimeField(
            initial=self.instance.date_added, disabled=True, required=False, label='Fecha de ingreso' 
        )
        self.fields['type'].disabled = True

class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramientas
        fields = ['name', 'price', 'type', 'stock', 'codigo_barras']
        labels = {
            'name': 'Nombre',
            'type': 'Tipo',
            'price': 'Precio',
            'stock': 'Stock',
            'codigo_barras':'Codigo Barras'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_added'] = forms.DateTimeField(
            initial=self.instance.date_added, disabled=True, required=False, label='Fecha de ingreso'
        )

class PinturaForm(forms.ModelForm):
    class Meta:
        model = Pinturas
        fields = ['name', 'price', 'type', 'stock', 'codigo_barras']
        labels = {
            'name': 'Nombre',
            'type': 'Tipo',
            'price': 'Precio',
            'stock': 'Stock',
            'codigo_barras':'Codigo Barras'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_added'] = forms.DateTimeField(
            initial=self.instance.date_added, disabled=True, required=False, label='Fecha de ingreso'
        )


class suplierForm(forms.ModelForm):
    class Meta:
        model = Suppliers
        fields = ['empresa', 'encargado', 'email', 'numero', 'direccion']



class ExcelUploadForm(forms.Form):
    file = forms.FileField(label="Archivo Excel")