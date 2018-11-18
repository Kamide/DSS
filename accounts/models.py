from django.db import models
from django.contrib.auth.models import User


class UserAcc(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    num_edits = models.IntegerField(default=0)
    recent_doc1 = models.CharField(max_length=30)
    recent_doc2 = models.CharField(max_length=30)
    recent_doc3 = models.CharField(max_length=30)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.TextField(blank=True)
    interests = models.TextField(max_length=100, blank=True)

    def __str__(self):
        return str(self.user) + ' ' + self.picture + ' ' + self.interests
