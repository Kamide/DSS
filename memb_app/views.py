from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import MembAppForm
from .models import MembApp
from accounts.models import Profile
from django.contrib.auth.models import User


# prompt for user to fill out application
# application's applicant name and interests are automatically filled behind the scenes
# is_pending flag set to true - user who sent application has to wait for a response before applying again (if denied)
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


# redirects SU to new page which is populated with list of pending applications
# when a single item is clicked, single_application() func. gets called (see below)
@login_required
def manage_applications(request):
    if not request.user.profile.has_su_rights():  # user must be SU to access page (prevents access thru URL)
        raise PermissionDenied

    applications_qs = MembApp.objects.all().filter(is_pending=True)
    context = {'applications_qs': applications_qs}
    return render(request, "memb_app/manage.html", context)


# opens a specific user's application in a new page (name passed thru url)
@login_required
def single_application(request, name, template='memb_app/single_application.html'):
    if not request.user.profile.has_su_rights():  # user must be SU to access page (prevents access thru URL)
        raise PermissionDenied

    person = User.objects.get(username=name)
    app = MembApp.objects.get(applicant=person)
    context = {'app': app}
    return render(request, template, context)


# if SU approves, this function gets called - turns a GU into an OU automatically
@login_required
def approve(request, name):
    if not request.user.profile.has_su_rights():  # user must be SU to access page (prevents access thru URL)
        raise PermissionDenied

    person = User.objects.get(username=name)  # gets applicant User object
    app = MembApp.objects.get(applicant=person)  # gets applicant's Membership Application object
    profile = Profile.objects.get(user=app.applicant)  # gets applicant's Profile
    profile.cohort = 1  # applicant is now an OU (enum GU = 0, OU = 1, SU = 2)
    profile.save()  # commits changes to database
    MembApp.objects.all().filter(applicant=person).delete()  # application no longer needed, deleted for space
    messages.success(request, f'Approved! {name} is now an OU.')  # success msg to SU
    return render(request, "accounts/index.html")  # return to homepage


@login_required
def deny(request, name):
    if not request.user.profile.has_su_rights(): # user must be SU to access page (prevents access thru URL)
        raise PermissionDenied

    person = User.objects.get(username=name)  # gets applicant User object
    app = MembApp.objects.get(applicant=person)  # gets applicant's Membership Application object
    app.is_pending = False  # sets flag to false; applicant can apply again
    app.save()  # commits changes to DB
    MembApp.objects.all().filter(applicant=person).delete()  # deletes application
    messages.success(request, f'Denied! Please message {name} to inform them.')  # reminds SU to message GU of denial
    return render(request, "accounts/index.html") # return to homepage
