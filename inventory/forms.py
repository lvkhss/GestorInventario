from django import forms
from .models import *

TIPOS_PRODUCTO = (
    ('Sellantes', 'Sellante'),
    ('Herramientas', 'Herramienta'),
    ('Pinturas', 'Pintura'),
)

class ProductoForm(forms.Form):
    name = forms.CharField(label="Nombre", max_length=200)
    price = forms.IntegerField(label="Precio")
    type = forms.ChoiceField(label="Tipo", choices=TIPOS_PRODUCTO)
    date_added = forms.DateTimeField(label='Fecha de ingreso', initial=now, required=False, disabled=True,)

class SellanteForm(forms.ModelForm):
    class Meta:
        model = Sellantes
        fields = ('name', 'price', 'type')
        labels = {
            'name': 'Nombre',
            'type': 'Tipo',
            'price': 'Precio',
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
        fields = ('name', 'price', 'type')
        labels = {
            'name': 'Nombre',
            'type': 'Tipo',
            'price': 'Precio',
        } 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_added'] = forms.DateTimeField(
            initial=self.instance.date_added, disabled=True, required=False, label='Fecha de ingreso'
        )

class PinturaForm(forms.ModelForm):
    class Meta:
        model = Pinturas
        fields = ('name', 'price', 'type')
        labels = {
            'name': 'Nombre',
            'type': 'Tipo',
            'price': 'Precio',
        } 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_added'] = forms.DateTimeField(
            initial=self.instance.date_added, disabled=True, required=False, label='Fecha de ingreso'
        )