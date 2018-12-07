from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Document
from django.contrib.auth.models import User
from .forms import RemoveUserForm
import filecmp
from dss.views import paginate


def index(request):
    context = {'docs': Document.objects.all()}
    return render(request, 'documents/dss.html', context)


class DocListView(ListView):
    model = Document
    template_name = 'documents/docs.html'
    context_object_name = 'docs'
    ordering = ['-view_count']

    def get_context_data(self, **kwargs):
        filters = {
            'title': False,
            'author': False,
            'content': False,
        }

        context = super().get_context_data(**kwargs)
        docs = self.get_queryset()
        search = self.request.GET.get('search')
        criteria = self.request.GET.getlist('criteria')
        search_criteria = ''
        for c in criteria:
            filters[c] = True
            search_criteria += '&criteria=' + c

        if search is None or search == '' or search_criteria == '' or self.request.user.is_anonymous or self.request.user.profile.is_gu() or self.request.user.profile.is_locked:
            search = ''
            filters['title'] = filters['content'] = True
            filters['author'] = False
        else:
            # Django: A Q object (django.db.models.Q) is an object used to
            # encapsulate a collection of keyword arguments.
            queries = search.split()
            results = Q()
            for query in queries:
                if filters['title']:
                    results = results | Q(title__icontains=query)
                if filters['author']:
                    results = results | Q(owner__username__icontains=query)
                if filters['content']:
                    results = results | Q(content__icontains=query)
            if filters['author']:
                docs = docs.filter(results)
            else:
                docs = docs.filter(results, owner=self.request.user)
            if docs.count() < 1:
                messages.error(self.request, f'Sorry, no results were found for {search}.')

        context['search'] = search
        context['filters'] = filters
        context['search_criteria'] = search_criteria
        context[self.context_object_name], context['count'], context['sequence'] = paginate(self.request, docs, default_count=15)
        return context


class DocDetailView(DetailView):
    model = Document
    form_class = RemoveUserForm

    def dispatch(self, request, *args, **kwargs):
        doc = self.get_object()
        if not self.request.user.is_anonymous and self.request.user.profile.is_locked and self.request.user.profile.doc_to_fix != doc.id:
            raise PermissionDenied
        else:
            doc.view_count += 1
            doc.save()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc = self.get_object()
        can_edit = doc.users_that_write.filter(id=self.request.user.id)
        if can_edit.exists():
            context['canedit'] = True
        else:
            context['canedit'] = False
        context['remove_user_form'] = self.form_class(doc=doc)
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
                with doc.txt.open() as f:
                    text = list(f)
                    text = b''.join(text)
                    text = text.decode()
                    text = text.replace('\r','')
                    text = text.splitlines()
                    size = len(text)
                with doc.cur_ver.open() as f:
                    text_prev = list(f)
                    text_prev = b''.join(text_prev)
                    text_prev = text_prev.decode()
                    text_prev = text_prev.replace('\r','')
                    text_prev = text_prev.splitlines()
                    size_prev = len(text_prev)
                if size - size_prev > 0:
                    remove = size - size_prev
                else:
                    add = size_prev - size
                cmds = []
                index = 0
                while add > 0 or remove > 0:
                    if remove > 0:
                        for word in text:
                            if index >= size_prev or word != text_prev[index]:
                                cmds.append("remove "+str(index))
                                remove -= 1
                                text.pop(index)
                                if remove == 0:
                                    break
                            else:
                                index += 1
                    elif add > 0:
                        added = 0
                        for word in text_prev:
                            if index >= size or word != text[index]:
                                cmds.append("add "+str(index+added)+' '+str(word))
                                add -= 1
                                text.insert(index+added, str(word))
                                added += 1
                                if add == 0:
                                    break
                            else:
                                index += 1
                index = len(text_prev)-1
                print(text)
                print(text_prev)
                for word in reversed(text):
                    if word != text_prev[index]:
                        cmds.append("update " + str(index) + ' '+str(text_prev[index]))
                    index -= 1

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
            doc = self.get_object()
            version = doc.version
            with doc.cur_ver.open() as f:
                #current = list(filter(None, (line.rstrip() for line in f)))
                current = list(f)
                current = b''.join(current)
                current = current.decode()
                current = current.replace('\r', '')
                current = current.splitlines()
            with doc.cmd_txt.open() as f:
                #commands = list(filter(None, (line.rstrip() for line in f)))
                commands = list(f)
                commands = b''.join(commands)
                commands = commands.decode()
                commands = commands.replace('\r', '')
                commands = commands.splitlines()
            commands.reverse()
            while version > int(request.POST['Version']):
                for cmd in commands:
                    if version <= int(request.POST['Version']):
                        break
                    action = cmd.split()
                    if action[0] == 'remove':
                        current.pop(int(action[1]))
                    elif action[0] == 'add':
                        current.insert(int(action[1]), ' '.join(action[2:]))
                    elif action[0] == 'update':
                        current[int(action[1])] = ' '.join(action[2:])
                    else:
                        version -= 1
            doc.old_ver = '\n'.join(current)
            doc.save()
            return redirect('version/?&version='+str(request.POST['Version']))
        elif request.POST.get("Kick"):
            evictions = request.POST.getlist('users_that_write')
            if evictions:
                evicted = []
                for u_id in evictions:
                    doc.users_that_write.remove(u_id)
                    evicted.append(User.objects.get(id=u_id).username)

                if len(evicted) > 1:
                    tense = ', '.join(evicted) + ' have'
                else:
                    tense = evicted[0] + ' has'
                messages.success(self.request, f'{tense} been removed from the list of users who can edit.')

        return redirect(doc.get_absolute_url())


class DocVersionView(DetailView):
    model = Document

    def dispatch(self, request, *args, **kwargs):
        doc = self.get_object()
        if not self.request.user.is_anonymous and self.request.user.profile.is_locked and self.request.user.profile.doc_to_fix != doc.id:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DocCreateView(LoginRequiredMixin, CreateView):
    model = Document
    fields = ['title', 'privacy', 'content']

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous and self.request.user.profile.is_locked:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.last_edited_by = self.request.user
        self.object = form.save()
        doc_txt = ContentFile(self.object.content)
        self.object.txt.save(self.object.title+'.txt', doc_txt)
        self.object.cur_ver.save(self.object.title + '_prev.txt', doc_txt)
        self.object.cmd_txt.save(self.object.title + '_cmd.txt', ContentFile(''))
        return super().form_valid(form)


class DocUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Document
    fields = ['title', 'content']

    def dispatch(self, request, *args, **kwargs):
        doc = self.get_object()
        if not self.request.user.is_anonymous and self.request.user.profile.is_locked and self.request.user.profile.doc_to_fix != doc.id:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_form'] = True
        return context

    def form_valid(self, form):
        form.instance.last_edited_by = self.request.user
        self.object.view_count -= 1
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

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous and self.request.user.profile.is_locked:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        doc = self.get_object()
        doc.view_count -= 1
        doc.save()
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
