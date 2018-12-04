from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MessageForm
from msg_system.models import Message
from documents.models import Document
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def compose(request):
    prefilled_to = request.GET.get('to')
    prefilled_msg = request.GET.get('showthis')
    doc_id = request.GET.get('inviteto')
    autofilled = {}
    is_invitation = False

    if prefilled_to is not None:
        autofilled['receiver'] = prefilled_to
    if prefilled_msg is not None:
        autofilled['msg_content'] = prefilled_msg
    if doc_id is not None:
        is_invitation = True

    if request.method == "POST":
        message_form = MessageForm(request.POST, is_invitation_msg=is_invitation)
        if message_form.is_valid():
            msg = message_form.save(commit=False)
            msg.sender = request.user
            msg.save()
            recipient = message_form.cleaned_data.get('receiver')

            if doc_id is not None:
                try:
                    doc = Document.objects.get(pk=''.join(filter(lambda x: x.isdigit(), doc_id)))
                    if doc.owner == request.user:
                        doc.pending_contributors.add(msg.receiver)
                        messages.success(request, f'The invitation to {recipient} has been successfully sent!')
                    else:
                        messages.error(request, f'You do not have the right to send invitations to this document.')
                        return redirect('compose')
                    return redirect(doc)
                except Document.DoesNotExist:
                    messages.error(request, f'You can not make invitations to invalid documents.')
                    msg.delete()
                    return redirect('compose')

            messages.success(request, f'The message to {recipient} has been successfully sent!')
            return redirect('sent')
    else:
        message_form = MessageForm(initial=autofilled, is_invitation_msg=is_invitation)

    context = {'message_form': message_form}

    return render(request, "msg_system/compose.html", context)


@login_required
def mailbox(request):
    return render(request, "msg_system/mailbox.html")


@login_required
def inbox(request):
    current_user = request.user.id
    inbox_qs = Message.objects.all().filter(receiver=current_user)
    context = {"inbox_qs": inbox_qs}
    return render(request, "msg_system/inbox.html", context)


@login_required
def sent(request):
    current_user = request.user.id
    sent_qs = Message.objects.all().filter(sender=current_user)
    context = {"sent_qs": sent_qs}
    return render(request, "msg_system/sent.html", context)
