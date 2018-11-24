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
        Profile.objects.create(user=instance)
        # get_or_create returns a tuple
        if instance.is_staff:
            instance.profile.make_su()
        else:
            instance.profile.make_gu()
        instance.profile.save()


@receiver(post_save, sender=Profile)
def update_user_rights(sender, instance, **kwargs):
    try:
        cohort = int(instance.get_cohort_value())
    except ValueError:
        cohort = instance.GUEST_USER

    # GU
    instance.user.is_staff = False
    instance.user.if_superuser = False

    if cohort >= instance.ORDINARY_USER:
        instance.user.is_superuser = True
    if cohort >= instance.SUPER_USER:
        instance.user.is_staff = True

    instance.user.save()
