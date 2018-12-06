from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import UpdateProfileForm, UpdateMembershipForm
from .models import Profile
from documents.models import Document


def index(request):
    # For debugging messages
    # messages.success(request, f'1')
    # messages.error(request, f'2')
    # messages.info(request, f'3')
    if not request.user.is_anonymous:
        return individuals(request, request.user.username, 'accounts/index.html')
    else:
        return render(request, 'accounts/index.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account {username} has been successfully created. You may now log in.')
            return redirect('login')
        else:
            messages.info(request, f'Please read over the username and password requirements, thank you.')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def settings(request):
    if request.method == 'POST':
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, f'Your profile settings have been saved!')
            return redirect('index')
    else:
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'accounts/settings.html', {'profile_form': profile_form})


def users(request):
    search = request.GET.get('search')

    if search is None or search == '' or request.user.is_anonymous or request.user.profile.is_gu() or request.user.profile.is_locked:
        search = ''
        list_of_users = User.objects.all()
    else:
        # Django: A Q object (django.db.models.Q) is an object used to
        # encapsulate a collection of keyword arguments.
        queries = search.split()
        results = Q()
        for query in queries:
            results = results | Q(username__icontains=query) | Q(profile__interests__icontains=query)
        list_of_users = User.objects.filter(results)

    if list_of_users.count() < 1:
        messages.error(request, f'Sorry, no results were found for {search}.')

    count = request.GET.get('count')

    if count is None:
        count = 10
    else:
        try:
            count = max(1, int(count))
        except ValueError:
            count = 10

    paginator = Paginator(list_of_users, count)
    page = request.GET.get('page')

    if page is None:
        page = 1
    else:
        try:
            page = max(0, int(page))
            if page > paginator.num_pages:
                page = paginator.num_pages
        except ValueError:
            page = 1

    list_of_users = paginator.get_page(page)

    # Get 5 numbers before and after the current page number
    # Ignore numbers that render invalid page numbers
    sequence = []
    for i in range(max(page-5, 1), min(page+5, paginator.num_pages) + 1):
        sequence.append(i)

    context = {
        'list_of_users': list_of_users,
        'search': search,
        'count': count,
        'sequence': sequence,
    }

    return render(request, 'accounts/users.html', context)


def individuals(request, name, template='accounts/individuals.html'):
    try:
        individual = User.objects.get(username=name)
    except User.DoesNotExist:
        individual = request.user
        messages.error(request, f"Sorry, we couldn't find a user named {name}.")
        messages.info(request, f'Now showing your profile page.')

    if request.method == 'POST' and request.user.profile.has_su_rights():
        um_form = UpdateMembershipForm(request.POST)
        if um_form.is_valid():
            cohort = request.POST.get('cohort')
            try:
                cohort = int(cohort)
                old_cohort = individual.profile.get_cohort()
                individual.profile.set_cohort(cohort)
                individual.profile.save()
                messages.success(request, f'{name} has been successfully changed from a {old_cohort} to a {Profile.COHORTS[cohort][1]}.')
            except ValueError:
                messages.error(request, f'Invalid group selected.')

            return redirect('individuals', name)
    else:
        um_form = UpdateMembershipForm(initial={'cohort': individual.profile.cohort})

    documents = Document.objects.filter(owner=individual).order_by('view_count').reverse()
    doc_count = documents.count()
    doc_views = documents.aggregate(Sum('view_count'))
    documents = documents[:3]
    if doc_count < 1:
        documents = Document.objects.order_by('view_count').reverse()[:3]
        has_docs = False
    else:
        has_docs = True

    context = {
        'individual': individual,
        'documents': documents,
        'has_docs': has_docs,
        'doc_count': doc_count,
        'doc_views': doc_views,
        'um_form': um_form,
    }

    return render(request, template, context)
