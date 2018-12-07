from django import template
from taboo.models import Taboo
from accounts.models import Profile
from documents.models import Document
import re

register = template.Library()


@register.filter(is_safe=True)
def censor_words(content):
    content_copy = content
    for taboo in Taboo.objects.all():
        word = taboo.word
        content_copy = re.sub('\\b'+word+'\\b', 'UNK', content_copy, flags=re.I)
    return content_copy
