from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Document(models.Model):
    PRIVACY_LEVELS = (('PUBLIC', 'Public'), ('RESTRICTED', 'Restricted'), ('SHARED', 'Shared'), ('PRIVATE', 'Private'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, unique=True)
    privacy = models.TextField(max_length=10, choices=PRIVACY_LEVELS)
    content = models.TextField()
    txt = models.FileField(null=True, upload_to='documents/')
    cur_ver = models.FileField(null=True, upload_to='documents/')
    cmd_txt = models.FileField(null=True, upload_to='documents/')
    version = models.IntegerField(default=000)
    lock_status = models.BooleanField(default=False)
    locked_by = models.TextField()
    edit_count = models.IntegerField(default=000)
    view_count = models.IntegerField(default=000)
    users_that_read = models.ManyToManyField(User, related_name="Readers")
    users_that_write = models.ManyToManyField(User, related_name="Contributors")
    pending_contributors = models.ManyToManyField(User, related_name="Invited")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('doc-detail', kwargs={'pk': self.pk})
