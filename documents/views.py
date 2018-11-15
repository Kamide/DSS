from django.shortcuts import render


def index(request):
    return render(request, 'documents/dss.html')


def docs(request):
    return render(request, 'documents/docs.html')