from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def local_urlize(value):
    return re.sub(r'(?m)/[^\s<>]+/', r'<a href="\g<0>">\g<0></a>', value)
