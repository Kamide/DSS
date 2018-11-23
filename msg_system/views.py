from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MessageForm


def compose(request):
    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message_form.save()
            recipient = message_form.cleaned_data.get('receiver')
            messages.success(request, f'The message to {recipient} has been successfully sent!')
    else:
        message_form = MessageForm()

    context = {'message_form': message_form}

    return render(request, "msg_system/compose.html", context)
