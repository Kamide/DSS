from django import forms
from .models import Document


class RemoveUserForm(forms.ModelForm):
    model = Document
    fields = ('users_that_write',)
    widgets = forms.Select(choices=Document.users_that_write)
