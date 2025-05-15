from django import forms
from .models import *

class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptops
        fields = ('type', 'price', 'status', 'issues')  # Exclude 'date_added'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_added'] = forms.DateTimeField(
            initial=self.instance.date_added, disabled=True, required=False
        )

class DesktopForm(forms.ModelForm):
    class Meta:
        model = Desktops
        fields = ('type', 'price', 'status', 'issues')  # Exclude 'date_added'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_added'] = forms.DateTimeField(
            initial=self.instance.date_added, disabled=True, required=False
        )

class MobileForm(forms.ModelForm):
    class Meta:
        model = Mobiles
        fields = ('type', 'price', 'status', 'issues')  # Exclude 'date_added'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_added'] = forms.DateTimeField(
            initial=self.instance.date_added, disabled=True, required=False
        )