from django.db import models
from django.contrib.auth.models import User


# membership application model w/ attributes: applicant (foreignkey), their interests, and extra details
# flag is_pending used to check if user already sent an application - prevents spam applications
class MembApp(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applicant")
    app_interests = models.CharField(max_length=100)
    extra_details = models.TextField(null=True)
    is_pending = models.BooleanField(default=False)



