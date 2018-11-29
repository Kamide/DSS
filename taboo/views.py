from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TabooForm
from .models import Taboo


def add_word(request):
    if request.method == "POST":
        taboo_form = TabooForm(request.POST)
        if taboo_form.is_valid():
            t = taboo_form.save(commit=False)
            words_to_add = t.word.split()
            if len(words_to_add) == 1:
                match_qs = Taboo.objects.all().filter(word=words_to_add[0])
                if match_qs.count() > 0:
                    messages.error(request, f'The word you entered is already on the list')
                else:
                    taboo_form.save()
                    messages.success(request, f'The word {words_to_add[0]} has been added to the list')
            else:
                duplicate_words = list()
                added_words = list()
                for w in words_to_add:
                    match_qs = Taboo.objects.all().filter(word=w)
                    if match_qs.count() == 0:
                        added_words.append(w)
                        t = Taboo(word=w)
                        t.save()
                    else:
                        duplicate_words.append(w)
                if len(added_words) > 0:
                    messages.success(request, f'The word(s) {added_words} have been added to the list!')
                if len(duplicate_words) > 0:
                    if len(duplicate_words) == len(words_to_add):
                        messages.error(request, f'All the words you tried to add are already on the list!')
                    else:
                        messages.error(request, f'The word(s) {duplicate_words} are already on the list')
            return redirect('/')
    else:
        taboo_form = TabooForm()

    context = {"taboo_form": taboo_form}
    return render(request, "taboo/add_word.html", context)


def del_word(request):
    if request.method == "POST":
        taboo_form = TabooForm(request.POST)
        if taboo_form.is_valid():
            t = taboo_form.save(commit=False)
            words_to_del = t.word.split()
            if len(words_to_del) == 1:
                match_qs = Taboo.objects.all().filter(word=words_to_del[0])
                if match_qs.count() == 0:
                    messages.error(request, f'The word {words_to_del[0]} does not exist on the list')
                else:
                    match_qs.delete()
                    messages.success(request, f'The word {words_to_del[0]} has been deleted off the list')
            else:
                non_exist_words = list()
                deleted_words = list()
                for w in words_to_del:
                    match_qs = Taboo.objects.all().filter(word=w)
                    if match_qs.count() != 0:
                        deleted_words.append(w)
                        match_qs.delete()
                    else:
                        non_exist_words.append(w)
                if len(deleted_words) > 0:
                        messages.success(request, f'The word(s) {deleted_words} have been deleted off the list')
                if len(non_exist_words) > 0:
                    if len(non_exist_words) == len(words_to_del):
                        messages.error(request, f'All the words you tried to delete do not exist on the list')
                    else:
                        messages.error(request, f'The word(s) {non_exist_words} do not exist on the list')
            return redirect('/')
    else:
        taboo_form = TabooForm()

    context = {"taboo_form": taboo_form}
    return render(request, "taboo/del_word.html", context)


def get_words(request):
    words_qs = Taboo.objects.all()
    context = {"words_qs": words_qs}
    return render(request, "taboo/taboo_list.html", context)
