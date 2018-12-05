from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MembAppForm
from .models import MembApp
from accounts.models import Profile
from django.contrib.auth.models import User


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


def manage_applications(request):
    applications_qs = MembApp.objects.all().filter(is_pending=True)
    context = {'applications_qs': applications_qs}
    return render(request, "memb_app/manage.html", context)


def single_application(request, name, template='memb_app/single_application.html'):
    person = User.objects.get(username=name)
    app = MembApp.objects.get(applicant=person)
    context = {'app': app}
    return render(request, template, context)


def approve(request, name):
    person = User.objects.get(username=name)
    app = MembApp.objects.get(applicant=person)
    profile = Profile.objects.get(user=app.applicant)
    profile.cohort = 1
    profile.save()
    MembApp.objects.all().filter(applicant=person).delete()
    messages.success(request, f'Approved! {name} is now an OU')
    return render(request, "accounts/index.html")


def deny(request, name):
    person = User.objects.get(username=name)
    app = MembApp.objects.get(applicant=person)
    app.is_pending = False
    app.save()
    MembApp.objects.all().filter(applicant=person).delete()
    messages.success(request, f'Denied! Please message {name} to inform them')
    return render(request, "accounts/index.html")

