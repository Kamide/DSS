from django import forms
from .models import MembApp


class MembAppForm(forms.ModelForm):
    class Meta:
        model = MembApp
        fields = ['extra_details']
        labels = {
            'extra_details': 'More Details About Yourself'
        }
