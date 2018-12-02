from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.core.files.base import ContentFile
from .models import Document
import filecmp


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
            doc.view_count -= 1
            doc.save()
            messages.success(request, f'Document Successfully Locked')
        elif request.POST.get("Unlock"):
            if self.request.user.username == doc.locked_by or self.request.user.profile.is_su():
                doc.lock_status = False
                doc.locked_by = ""
                doc.view_count -= 1
                messages.success(request, f'Document Successfully Unlocked')
                doc.save()
            else:
                messages.error(request, f'You did not lock this document initially')
        elif request.POST.get("Update"):
            if self.request.user.username == doc.locked_by and not filecmp.cmp(doc.txt.name, doc.cur_ver.name):
                add = 0
                remove = 0
                update = 0
                with doc.txt.open() as f:
                    text = list(filter(None, (line.rstrip() for line in f)))
                    size = len(text)
                with doc.cur_ver.open() as f:
                    text_prev = list(filter(None, (line.rstrip() for line in f)))
                    size_prev = len(text_prev)
                if size - size_prev > 0:
                    remove = size - size_prev
                else:
                    add = size_prev - size
                for word in text_prev:
                    if word not in text:
                        update += 1
                cmds = []
                index = 0
                messages.success(request, remove)
                while add > 0 or remove > 0:
                    if remove > 0:
                        for word in text:
                            if index >= size_prev or word != text_prev[index]:
                                cmds.append("remove "+str(index))
                                remove -= 1
                                if remove == 0:
                                    break
                            else:
                                messages.success(request, f'Works')
                                index += 1
                    elif add > 0:
                        for word in text:
                            if word != text_prev[index]:
                                cmds.append("add "+str(index))
                                add -= 1
                                if add == 0:
                                    break
                            else:
                                index += 1
                index = 0
                while update > 0:
                    for word in text:
                        if word != text_prev[index]:
                            cmds.append("update " + str(index) + ' '+str(text_prev[index].decode("utf-8")))
                            update -= 1
                            if update == 0:
                                break
                cmds.reverse()
                with doc.cmd_txt.open('a') as f:
                    f.write(str(doc.version)+'\n')
                    for command in cmds:
                        f.write(command+'\n')
                doc.version += 1
                doc.cur_ver.delete()
                cur_txt = ContentFile(doc.content)
                doc.cur_ver.save(doc.title + '_prev.txt', cur_txt)
                doc.save()
        elif request.POST.get("Version"):
            messages.success(request, f'Works')
        return redirect(doc.get_absolute_url())


class DocCreateView(LoginRequiredMixin, CreateView):
    model = Document
    fields = ['title', 'privacy', 'content']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        doc_txt = ContentFile(self.object.content)
        self.object.txt.save(self.object.title+'.txt', doc_txt)
        self.object.cur_ver.save(self.object.title + '_prev.txt', doc_txt)
        self.object.cmd_txt.save(self.object.title + '_cmd.txt', ContentFile(''))
        return super().form_valid(form)



class DocUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Document
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        self.object.txt.delete()
        doc_txt = ContentFile(self.object.content)
        self.object.txt.save(self.object.title+'.txt', doc_txt)
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
            doc.txt.delete()
            doc.cmd_txt.delete()
            doc.cur_ver.delete()
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
            return redirect(doc.get_absolute_url())
        elif request.POST.get("Denied"):
            doc.pending_contributors.remove(self.request.user)
            messages.success(request, f'Denied')
            doc.save()
        return redirect('docs')


def docs(request):
    return render(request, 'documents/docs.html')
