from django import forms
from .models import Taboo


# accompanying form for Taboo model/table
class TabooForm(forms.ModelForm):
    class Meta:
        model = Taboo
        fields = ['word']