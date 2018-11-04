from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Profile


# Adds the attributes of Profile (picture, interests)
# to registering user. Their group will be 'Guest Users'.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        try:
            gu = Group.objects.get(name='Guest Users')
        except Group.DoesNotExist:
            pass
        else:
            instance.groups.add(gu)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
