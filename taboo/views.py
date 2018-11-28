from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TabooForm
from .models import Taboo


def add_word(request):
    if request.method == "POST":
        taboo_form = TabooForm(request.POST)
        if taboo_form.is_valid():
            t = taboo_form.save(commit = False)
            word_to_add = t.word
            match_qs = Taboo.objects.all().filter(word = word_to_add)
            if match_qs.count() > 0:
                messages.error(request, f'The word you entered is already on the list')
            else:
                taboo_form.save()
                word_added = taboo_form.cleaned_data.get('word')
                messages.success(request, f'The word {word_added} has been added to the list')
                return redirect('/')

    else:
        taboo_form = TabooForm()

    context = {"taboo_form": taboo_form}
    return render(request, "taboo/add_word.html", context)


def del_word(request):
    if request.method == "POST":
        taboo_form = TabooForm(request.POST)
        if taboo_form.is_valid():
            t = taboo_form.save(commit = False)
            word_to_del = t.word
            match_qs = Taboo.objects.all().filter(word = word_to_del)
            if match_qs.count() < 1:
                messages.error(request, f'The word you entered does not exist on the list')
            else:
                match_qs.delete()
                messages.success(request, f'The word {word_to_del} has been deleted off the list')
                return redirect('/')

    else:
        taboo_form = TabooForm()

    context = {"taboo_form": taboo_form}
    return render(request, "taboo/del_word.html", context)


def get_words(request):
    words_qs = Taboo.objects.all()
    context = {"words_qs": words_qs}
    return render(request, "taboo/taboo_list.html", context)

