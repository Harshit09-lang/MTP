from django import forms 
from .models import MLmodel,Data

class MLfileForm(forms.ModelForm):
    class Meta:
        model = MLmodel
        fields = '__all__'

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = '__all__'