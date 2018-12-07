from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Document
from taboo.models import Taboo
from accounts.models import Profile
import re


def has_taboo_words(content):
    taboos = [str(taboo).upper() for taboo in Taboo.objects.all()]
    content_copy = re.sub(r'[^\w\s]', ' ', content).upper().split()
    return not set(taboos).isdisjoint(content_copy)


def unlock_profiles(doc_id):
    profiles = Profile.objects.filter(doc_to_fix=doc_id)
    if profiles.exists():
        for p in profiles:
            p.is_locked = False
            p.doc_to_fix = None
            p.save()


@receiver(post_save, sender=Document)
def contains_taboo_words(sender, instance, **kwargs):
    infringed = has_taboo_words(instance.content) or has_taboo_words(instance.title)
    id = instance.id
    last_edited_by = instance.last_edited_by

    if infringed and last_edited_by is not None:
        profile = Profile.objects.get(user=last_edited_by)
        profile.is_locked = True
        profile.doc_to_fix = id
        profile.save()
    else:
        unlock_profiles(id)


@receiver(pre_delete, sender=Document)
def free_locked_profiles(sender, instance, **kwargs):
    unlock_profiles(instance.id)
