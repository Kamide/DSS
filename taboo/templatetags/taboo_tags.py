from django import template
from taboo.models import Taboo
from accounts.models import Profile
from documents.models import Document
import re

register = template.Library()


# using regex to substitute taboo words with 'UNK'
@register.filter(is_safe=True)
def censor_words(content):
    content_copy = content  # censored content gets displayed (original content untouched) - keeps data integrity
    for taboo in Taboo.objects.all():
        word = taboo.word
        # if taboo word pattern found, replaces with 'UNK'
        # respects word boundaries, i.e if taboo word is subset of another word, it won't get censored
        content_copy = re.sub('\\b'+word+'\\b', 'UNK', content_copy, flags=re.I)
    return content_copy
