from django import forms
from .models import Message
from django.contrib.auth.models import User
from accounts.models import Profile


# Message Form - for the message system; this is what the user fills out
# user can select who to send to (receiver), reason for message, and type what he wants to say (msg_content)
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'reason', 'msg_content']
        labels = {
            'msg_content': 'Message content'
        }

    # checks if user needs to contact a user that can process complaints (OU for docs and SU for general)
    # e.g, reporting someone: valid receivers are SUs only.
    def __init__(self, *args, **kwargs):
        is_contacting_authority = kwargs.pop('is_contacting_authority')
        super(MessageForm, self).__init__(*args, **kwargs)
        if is_contacting_authority:
            users = User.objects.all()
            self.fields['receiver'].queryset = User.objects.filter(profile__cohort__gte=Profile.ORDINARY_USER)
        else:
            self.fields['receiver'].queryset = User.objects.all()
