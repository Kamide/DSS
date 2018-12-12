from django import forms
from .models import MembApp


# form that goes with the model
# applicant only fills out extra details they want the SU to read, all other fields get populated automatically
class MembAppForm(forms.ModelForm):
    class Meta:
        model = MembApp
        fields = ['extra_details']
        labels = {
            'extra_details': 'More Details About Yourself'
        }
