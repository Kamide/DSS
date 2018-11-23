from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Profile


#
#
@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    """Adds the attributes of Profile (picture, interests)
    to registering user. Their group will be 'Guest Users'.
    Running the following command in a terminal will put
    the user in the 'Super Users' group:
        $ python manage.py createsuperuser"""
    if created:
        Profile.objects.create(user=instance)
        # get_or_create returns a tuple
        if instance.is_staff:
            cohort, created = Group.objects.get_or_create(name='Super Users')
        else:
            cohort, created = Group.objects.get_or_create(name='Guest Users')
        instance.groups.add(cohort)


@receiver(post_save, sender=User)
def save_user(sender, instance, **kwargs):
    instance.profile.save()
