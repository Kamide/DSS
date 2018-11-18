from django.db import models
from accounts.models import Profile

class Document(models.Model):
    PRIVACY_LEVELS = (('PUB', 'Public'), ('R', 'Restricted'), ('S', 'Shared'), ('PRIV', 'Private'))
    owner = models.CharField(max_length=30, primary_key=True)
    title = models.CharField(max_length=30, primary_key=True)
    privacy = models.CharField(max_length=4, choices=PRIVACY_LEVELS)
    content = models.CharField(max_length=100)
    version = models.IntegerField(default=000)
    lock_status = models.BooleanField(default=False)
    locked_by = models.CharField(max_length=30)
    edit_count = models.IntegerField(default=000)
    view_count = models.IntegerField(default=000)
    user = models.ForeignKey(Profile)
    users_that_read = models.ManyToManyField(user)
    users_that_edit = models.ManyToManyField(user)

    def __str__(self):
        return self.owner + self.title
