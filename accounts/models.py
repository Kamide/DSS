from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.URLField(blank=True)
    interests = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.user) + ' ' + self.picture + ' ' + self.interests
