from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.auth.models import Group
from memb_app.models import MembApp

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
def get_cohort_pluralized(user):
    try:
        return user.profile.get_cohort() + 's'
    except AttributeError:
        return str(user) + " (No Cohort Found)"


@register.filter(is_safe=True)
def get_cohort_initials(user, sep=''):
    try:
        return acronymize(user.profile.get_cohort(), sep)
    except AttributeError:
        return str(user) + " (No Cohort Found)"

# @register.filter(is_safe=True)
# def get_cohort_initials(user, sep=''):
#     return acronymize(user.profile.get_cohort(), sep)


@register.filter(is_safe=True)
def is_gu(user):
    try:
        return user.profile.is_gu()
    except AttributeError:
        return False


@register.filter(is_safe=True)
def is_ou(user):
    try:
        return user.profile.is_ou()
    except AttributeError:
        return False


@register.filter(is_safe=True)
def is_su(user):
    try:
        return user.profile.is_su()
    except AttributeError:
        return False


@register.filter(is_safe=True)
def has_su_rights(user):
    try:
        return user.profile.has_su_rights()
    except AttributeError:
        return False


@register.filter(is_safe=True)
def has_ou_rights(user):
    try:
        return user.profile.has_ou_rights()
    except AttributeError:
        return False


@register.filter(is_safe=True)
def has_gu_rights(user):
    try:
        return user.profile.has_gu_rights()
    except AttributeError:
        return False


@register.filter(is_safe=True)
def is_locked_out(user):
    try:
        return user.profile.locked()
    except AttributeError:
        return False


@register.filter(is_safe=True)
def already_applied(user):
    apps_qs = MembApp.objects.all().filter(applicant=user.profile.get_userid())
    if apps_qs.count() > 0:
        return True
    else:
        return False
