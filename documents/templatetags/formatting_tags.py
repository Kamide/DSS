from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def preserve_spaces(value):
    return value.replace(' ', '&nbsp;')


@register.filter(is_safe=True)
@stringfilter
def parse_formatting_tags(value):
    return re.sub(r'(?m)\[b\](.+?)\[\/b\]', r'<strong>\1</strong>', value)
