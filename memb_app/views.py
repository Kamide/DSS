from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import MembAppForm
from .models import MembApp
from accounts.models import Profile
from django.contrib.auth.models import User


@login_required
def apply(request):
    if request.method == "POST":
        memb_app_form = MembAppForm(request.POST)
        if memb_app_form.is_valid():
            application = memb_app_form.save(commit=False)
            application.applicant = request.user
            profile = Profile.objects.get(user=request.user)
            application.app_interests = profile.interests
            application.is_pending = True
            application.save()

            messages.success(request, f'Application sent! An SU will review it and get back to you!')
            return redirect('/')
    else:
        memb_app_form = MembAppForm()

    context = {"memb_app_form": memb_app_form}
    return render(request, "memb_app/apply.html", context)


@login_required
def manage_applications(request):
    if not request.user.profile.has_su_rights():
        raise PermissionDenied

    applications_qs = MembApp.objects.all().filter(is_pending=True)
    context = {'applications_qs': applications_qs}
    return render(request, "memb_app/manage.html", context)


@login_required
def single_application(request, name, template='memb_app/single_application.html'):
    if not request.user.profile.has_su_rights():
        raise PermissionDenied

    person = User.objects.get(username=name)
    app = MembApp.objects.get(applicant=person)
    context = {'app': app}
    return render(request, template, context)


@login_required
def approve(request, name):
    if not request.user.profile.has_su_rights():
        raise PermissionDenied

    person = User.objects.get(username=name)
    app = MembApp.objects.get(applicant=person)
    profile = Profile.objects.get(user=app.applicant)
    profile.cohort = 1
    profile.save()
    MembApp.objects.all().filter(applicant=person).delete()
    messages.success(request, f'Approved! {name} is now an OU.')
    return render(request, "accounts/index.html")


@login_required
def deny(request, name):
    if not request.user.profile.has_su_rights():
        raise PermissionDenied

    person = User.objects.get(username=name)
    app = MembApp.objects.get(applicant=person)
    app.is_pending = False
    app.save()
    MembApp.objects.all().filter(applicant=person).delete()
    messages.success(request, f'Denied! Please message {name} to inform them.')
    return render(request, "accounts/index.html")
