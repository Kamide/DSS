from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserUpdateForm, UpdateProfileForm


def index(request):
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
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def settings(request):
    user_form = UserUpdateForm()
    profile_form = UpdateProfileForm()
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/settings.html', context)

def users(request):
    return render(request, 'accounts/users.html')

