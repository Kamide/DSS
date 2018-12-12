from django.db import models
from django.contrib.auth.models import User

MESSAGE_REASONS = (
    ('OTHER', 'Other'),
    ('SUGGEST TABOO WORDS', 'Suggest Taboo Words'),
    ('FILE A COMPLAINT', 'File A Complaint')
)


# Message model (or table) with attributes: sender, receiver, reason and message content
# reason can only be above choices
# foreign keys: sender and receiver (points to User table)
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    reason = models.CharField(max_length=20, choices=MESSAGE_REASONS, default='other')
    msg_content = models.TextField(default='Type message here')

    def __str__(self):
        return self.sender.username + ' ' + self.receiver.username + ' ' + self.msg_content
