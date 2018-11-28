from django import forms
from .models import Taboo


class TabooForm(forms.ModelForm):
    class Meta:
        model = Taboo
        fields = ['word']