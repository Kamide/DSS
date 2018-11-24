from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Adds Profile to registering user.
    Their cohort will be 'Guest Users'.
    Running the following terminal command
    will put the user in the 'Super Users' cohort:
        $ python manage.py createsuperuser"""
    if created:
        if instance.is_staff or instance.is_superuser:
            Profile.objects.create(user=instance, cohort=Profile.SUPER_USER)
        else:
            Profile.objects.create(user=instance)
        instance.profile.save()


@receiver(post_save, sender=Profile)
def update_user_rights(sender, instance, **kwargs):
    # GU
    instance.user.is_superuser = False
    instance.user.is_staff = False

    if instance.has_ou_rights():
        instance.user.is_superuser = True
    if instance.has_su_rights():
        instance.user.is_staff = True

    instance.user.save()
