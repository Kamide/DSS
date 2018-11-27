from django.db import models
from django.contrib.auth.models import User

MESSAGE_REASONS = (
    ('OTHER', 'Other'),
    ('SUGGEST TABOO WORDS', 'Suggest Taboo Words'),
    ('FILE A COMPLAINT', 'File A Complaint')
)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "sender")
    receiver = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "receiver")
    reason = models.CharField(max_length = 20, choices = MESSAGE_REASONS, default = 'other')
    msg_content = models.TextField(default = 'Type message here')
    receiver_archive = models.BooleanField(default = False)
    sender_archive = models.BooleanField(default = True)

    def __str__(self):
        return self.sender.username + ' ' + self.receiver.username + ' ' + self.msg_content


