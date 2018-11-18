from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    PRIVACY_LEVELS = (('PUB', 'Public'), ('R', 'Restricted'), ('S', 'Shared'), ('PRIV', 'Private'))
    owner = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    privacy = models.CharField(max_length=4, choices=PRIVACY_LEVELS)
    content = models.CharField(max_length=100)
    version = models.IntegerField(default=000)
    lock_status = models.BooleanField(default=False)
    locked_by = models.CharField(max_length=30)
    edit_count = models.IntegerField(default=000)
    view_count = models.IntegerField(default=000)
    users_that_read = models.ManyToManyField(User)
    users_that_write = models.ManyToManyField(User, related_name="Contributors")

    def __str__(self):
        return self.owner + self.title

    class Meta:
        unique_together = (("owner", "title"),)
