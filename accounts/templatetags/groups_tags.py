from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def acronymize(value, sep=''):
    """Extracts the capital letters in a string."""

    combo = str(value)
    words = combo.split(' ')
    acronym = ''

    for w in words:
        if w != '':
            initial = w[0]
            if initial.isupper():
                acronym += initial + sep

    return acronym


@register.filter(is_safe=True)
def has_group(user):
    return user.groups.all().exists()


@register.filter(is_safe=True)
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(is_safe=True)
def get_group_name(user):
    if has_group(user):
        return user.groups.all()[0]
    else:
        return "Groupless"


@register.filter(is_safe=True)
def get_group_initials(user):
    if has_group(user):
        return acronymize(get_group_name(user))
    else:
        return "Groupless"
