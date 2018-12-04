from django import template
from taboo.models import Taboo
from accounts.models import Profile
from documents.models import Document
import re

register = template.Library()


@register.filter(is_safe=True)
def censor_words(content):
    content_copy = ''.join(content)
    for taboo in Taboo.objects.all():
        word = taboo.word
        content_copy = re.sub('\\b'+word+'\\b', 'UNK', content_copy, flags=re.I)
    return content_copy


@register.filter(is_safe=True)
def contains_taboo_words(title):
    doc = Document.objects.get(title=title)
    doc_censored_content = censor_words(doc.content)
    last_edited_by = doc.last_edited_by
    if last_edited_by:
        word_list = doc_censored_content.split()
        for word in word_list:
            if word == 'UNK':
                profile = Profile.objects.get(user=last_edited_by)
                profile.is_locked = True
                profile.doc_to_fix = title
                profile.save()
                return
        profile = Profile.objects.get(user=last_edited_by)
        if profile.is_locked is True and profile.doc_to_fix == title:
            profile.is_locked = False
            profile.save()
    return
