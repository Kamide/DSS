from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "sender")
    receiver = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "receiver")
    msg_content = models.TextField(default = 'Type message here')

    def __str__(self):
        return self.sender.username + ' ' + self.receiver.username + ' ' + self.msg_content


