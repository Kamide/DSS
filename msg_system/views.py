from django.shortcuts import render, redirect
from .forms import MessageForm


def compose(request):
    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message_form.save()

    else:
        message_form = MessageForm()

    context = {'message_form': message_form}

    return render(request, "msg_system/compose.html", context)
