from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Document
from accounts.models import Profile


def index(request):
    context = {'docs': Document.objects.all()}
    return render(request, 'documents/dss.html', context)


class DocListView(ListView):
    model = Document
    template_name = 'documents/docs.html'
    context_object_name = 'docs'
    ordering = ['-view_count']


class DocDetailView(DetailView):
    model = Document

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc = self.get_object()
        doc.view_count += 1
        doc.save(update_fields=['view_count'])
        can_edit = doc.users_that_write.filter(id=self.request.user.id)
        if can_edit.exists():
            context['canedit'] = True
        else:
            context['canedit'] = False
        return context

    def post(self, request, *args, **kwargs):
        doc = self.get_object()
        if request.POST.get("Lock"):
            doc.lock_status = True
            doc.locked_by = self.request.user.username
            doc.save()
            messages.success(request, f'Document Successfully Locked')
        elif request.POST.get("Unlock"):
            if self.request.user.username == doc.locked_by or self.request.user.profile.is_su():
                doc.lock_status = False
                doc.locked_by = ""
                messages.success(request, f'Document Successfully Unlocked')
                doc.save()
            else:
                messages.error(request, f'You did not lock this document initially')
        return redirect(doc.get_absolute_url())


class DocCreateView(LoginRequiredMixin, CreateView):
    model = Document
    fields = ['title', 'privacy', 'content']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DocUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Document
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        doc = self.get_object()
        if self.request.user == doc.owner or self.request.user in doc.users_that_write.all():
            return True
        return False


class DocDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Document
    success_url = '/'

    def test_func(self):
        doc = self.get_object()
        if self.request.user == doc.owner:
            return True
        return False


class DocInviteView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Document

    def test_func(self):
        doc = self.get_object()
        pending = doc.pending_contributors.filter(id=self.request.user.id)
        if pending.exists():
            return True
        return False

    def post(self, request, *args, **kwargs):
        doc = self.get_object()
        if request.POST.get("Accepted"):
            doc.pending_contributors.remove(self.request.user)
            doc.users_that_write.add(self.request.user)
            doc.save()
            messages.success(request, f'Accepted')
            return redirect(doc.get_absolute_url(self))
        elif request.POST.get("Denied"):
            doc.pending_contributors.remove(self.request.user)
            messages.success(request, f'Denied')
            doc.save()
        return redirect('docs')


def docs(request):
    return render(request, 'documents/docs.html')
