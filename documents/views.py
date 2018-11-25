from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Document


def index(request):
    context = {'docs': Document.objects.all()}
    return render(request, 'documents/dss.html', context)


class DocListView(ListView):
    model = Document
    template_name = 'documents/docs.html'
    context_object_name = 'docs'
    ordering = ['-edit_count']


class DocDetailView(DetailView):
    model = Document


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
        if self.request.user == doc.owner or self.request.user in doc.users_that_write.all():
            return True
        return False


def docs(request):
    return render(request, 'documents/docs.html')
