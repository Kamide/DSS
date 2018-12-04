from django import forms
from .models import Message
from django.contrib.auth.models import User
from accounts.models import Profile

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'reason', 'msg_content']

    def __init__(self, *args, **kwargs):
        is_invitation_msg = kwargs.pop('is_invitation_msg')
        super(MessageForm, self).__init__(*args, **kwargs)
        if is_invitation_msg:
            users = User.objects.all()
            self.fields['receiver'].queryset = User.objects.filter(profile__cohort__gte=Profile.ORDINARY_USER)
        else:
            self.fields['receiver'].queryset = User.objects.all()
