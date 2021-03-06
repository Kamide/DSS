from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture', 'interests']


class UpdateThemeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dark_theme_enabled']


class UpdateMembershipForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {
            'cohort': forms.RadioSelect
        }
        fields = ['cohort']
