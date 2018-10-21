from django.shortcuts import render


def index(request):
    return render(request, 'accounts/index.html')


def signup(request):
    return render(request, 'accounts/signup.html')
