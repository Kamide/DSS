from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Document(models.Model):
    PRIVACY_LEVELS = (('PUBLIC', 'Public'), ('RESTRICTED', 'Restricted'), ('SHARED', 'Shared'), ('PRIVATE', 'Private'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, unique=True)
    privacy = models.TextField(max_length=10, choices=PRIVACY_LEVELS)
    content = models.TextField()
    version = models.IntegerField(default=000)
    lock_status = models.BooleanField(default=False)
    locked_by = models.CharField(max_length=30)
    edit_count = models.IntegerField(default=000)
    view_count = models.IntegerField(default=000)
    users_that_read = models.ManyToManyField(User, related_name="Readers")
    users_that_write = models.ManyToManyField(User, related_name="Contributors")

    def __str__(self):
        return self.owner + self.title

    def get_absolute_url(self):
        return reverse('doc-detail', kwargs={'pk': self.pk})
