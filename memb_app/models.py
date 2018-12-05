from django.db import models
from django.contrib.auth.models import User



class MembApp(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applicant")
    app_interests = models.CharField(max_length=100)
    extra_details = models.TextField(null=True)
    is_pending = models.BooleanField(default=False)



