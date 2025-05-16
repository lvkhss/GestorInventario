from django import forms
from .models import *

class SellanteForm(forms.ModelForm):
    class Meta:
        model = Sellantes
        fields = ('type', 'price', 'status', 'issues')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_added'] = forms.DateTimeField(
            initial=self.instance.date_added, disabled=True, required=False
        )

class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramientas
        fields = ('type', 'price', 'status', 'issues')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_added'] = forms.DateTimeField(
            initial=self.instance.date_added, disabled=True, required=False
        )

class PinturaForm(forms.ModelForm):
    class Meta:
        model = Pinturas
        fields = ('type', 'price', 'status', 'issues')  # Exclude 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_added'] = forms.DateTimeField(
            initial=self.instance.date_added, disabled=True, required=False
        )