from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MessageForm
from msg_system.models import Message
from documents.models import Document
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


@login_required
def compose(request):
    if request.user.profile.is_locked:
        raise PermissionDenied

    prefilled_to = request.GET.get('to')
    prefilled_reason = request.GET.get('reason')
    prefilled_msg = request.GET.get('showthis')
    doc_id = request.GET.get('inviteto')
    autofilled = {}
    authority_wanted = False
    reset_msg = ''

    if prefilled_to is not None:
        autofilled['receiver'] = prefilled_to
    if prefilled_reason is not None:
        autofilled['reason'] = prefilled_reason
    if prefilled_msg is not None:
        autofilled['msg_content'] = prefilled_msg
    if prefilled_reason == 'FILE A COMPLAINT':
        reset_msg = 'Cancel Report'
        authority_wanted = True
    if doc_id is not None:
        reset_msg = 'Cancel Invitation'
        authority_wanted = True

    if request.method == "POST":
        message_form = MessageForm(request.POST, is_contacting_authority=authority_wanted)
        if message_form.is_valid():  # all user input fields are filled out
            msg = message_form.save(commit=False)
            msg.sender = request.user  # puts current user in sender field
            msg.save()
            recipient = message_form.cleaned_data.get('receiver')  # gets name of receiver for later success/fail msg

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
        message_form = MessageForm(initial=autofilled, is_contacting_authority=authority_wanted)

    context = {'message_form': message_form,
               'reset_msg': reset_msg}

    return render(request, "msg_system/compose.html", context)


@login_required
def mailbox(request):
    return render(request, "msg_system/mailbox.html")


@login_required
def inbox(request):
    if request.user.profile.is_locked:
        raise PermissionDenied

    current_user = request.user.id
    # queryset of all Message objects that have the receiver as the person currently viewing his mailbox
    inbox_qs = Message.objects.all().filter(receiver=current_user)
    context = {"inbox_qs": inbox_qs}
    return render(request, "msg_system/inbox.html", context)


@login_required
def sent(request):
    if request.user.profile.is_locked:
        raise PermissionDenied

    current_user = request.user.id
    # queryset of all Message objects that have the sender as the person currently viewing his mailbox
    sent_qs = Message.objects.all().filter(sender=current_user)
    context = {"sent_qs": sent_qs}
    return render(request, "msg_system/sent.html", context)
