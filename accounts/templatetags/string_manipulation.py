from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def acronymize(value, arg, sep=''):
    """Extracts the capital letters in a string."""

    combo = str(value) + ' ' + str(arg)
    words = combo.split(' ')
    acronym = ''
    initial = ''

    for w in words:
        if w != '':
            initial = w[0]
            if initial.isupper():
                acronym += initial + sep

    return acronym
