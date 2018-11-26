from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MessageForm
from msg_system.models import Message
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def compose(request):
    prefilled_msg = request.GET.get('showthis')

    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            msg = message_form.save(commit = False)
            msg.sender = request.user
            msg.save()
            recipient = message_form.cleaned_data.get('receiver')
            messages.success(request, f'The message to {recipient} has been successfully sent!')
            return redirect('/')
    else:
        if prefilled_msg is None:
            message_form = MessageForm() #Type message here
        else:
            message_form = MessageForm(initial={'msg_content': prefilled_msg})

    context = {'message_form': message_form}

    return render(request, "msg_system/compose.html", context)


def mailbox(request):

    current_user = request.user.id

    #Inbox
    inbox_qs = Message.objects.all().filter(receiver = current_user)

    #Sent
    sent_qs = Message.objects.all().filter(sender = current_user)

    context = {
        "inbox_qs": inbox_qs,
        "sent_qs": sent_qs
    }
    return render(request, "msg_system/mailbox.html", context)