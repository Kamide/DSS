from django import forms
from .models import Document


class RemoveUserForm(forms.ModelForm):
    class Meta:
        model = Document
        widgets = {
            'users_that_write': forms.CheckboxSelectMultiple
        }
        fields = ['users_that_write']

    def __init__(self, *args, **kwargs):
        doc = kwargs.pop('doc')
        super(RemoveUserForm, self).__init__(*args, **kwargs)
        self.fields['users_that_write'].label = ''
        if doc is not None:
            self.fields['users_that_write'].queryset = doc.users_that_write.all()
