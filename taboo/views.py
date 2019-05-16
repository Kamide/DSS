from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import TabooForm
from .models import Taboo


@login_required
def add_word(request):
    if not request.user.profile.has_su_rights():
        raise PermissionDenied

    if request.method == "POST":
        taboo_form = TabooForm(request.POST)
        if taboo_form.is_valid():
            t = taboo_form.save(commit=False)  # pauses commit to database to do additional work
            words_to_add = t.word.split()  # list of words (in case SU added multiple words at once)
            if len(words_to_add) == 1:  # only one word was entered
                match_qs = Taboo.objects.all().filter(word=words_to_add[0])  # checks if word already exists in list
                if match_qs.count() > 0:
                    messages.error(request, f'The word you entered is already on the list')
                else:
                    taboo_form.save()  # word doesn't exist on list, commits change
                    messages.success(request, f'The word {words_to_add[0]} has been added to the list')
            else:
                duplicate_words = list()  # empty list for catching words already on the list
                added_words = list()  # empty list for storing words successfully added
                for w in words_to_add:  # parsing thru list of inputted words
                    match_qs = Taboo.objects.all().filter(word=w)  # queryset of words that match word being added
                    if match_qs.count() == 0:  # queryset is empty; i.e word w isn't already in the list
                        added_words.append(w)  # add word w to successfully added words list
                        t = Taboo(word=w)  # add word w to actual database
                        t.save()  # commit change
                    else:
                        duplicate_words.append(w)  # queryset was not empty, i.e word w already on the list
                if len(added_words) > 0:  # displays successfully added word(s) given they exist
                    messages.success(request, f'The word(s) {added_words} have been added to the list!')
                if len(duplicate_words) > 0:  # displays word(s) already on the list
                    if len(duplicate_words) == len(words_to_add):
                        messages.error(request, f'All the words you tried to add are already on the list!')
                    else:
                        messages.error(request, f'The word(s) {duplicate_words} are already on the list')
            return redirect('/')
    else:
        taboo_form = TabooForm()

    context = {"taboo_form": taboo_form}
    return render(request, "taboo/add_word.html", context)


@login_required
def del_word(request):
    if not request.user.profile.has_su_rights():
        raise PermissionDenied

    if request.method == "POST":
        taboo_form = TabooForm(request.POST)
        if taboo_form.is_valid():
            t = taboo_form.save(commit=False)
            words_to_del = t.word.split()  # list of words SU trying to delete
            if len(words_to_del) == 1:  # SU only deleting one word
                match_qs = Taboo.objects.all().filter(word=words_to_del[0])
                if match_qs.count() == 0:  # word trying to get deleted not on list - error msg thrown
                    messages.error(request, f'The word {words_to_del[0]} does not exist on the list')
                else:
                    match_qs.delete()  # word present on the list, gets deleted
                    messages.success(request, f'The word {words_to_del[0]} has been deleted off the list')
            else:
                non_exist_words = list()  # empty list of potential words that do not exist on the list
                deleted_words = list()  # empty list of potential successfully deleted words
                for w in words_to_del:
                    match_qs = Taboo.objects.all().filter(word=w)  # checks if word w exists in taboo list or not
                    if match_qs.count() != 0:  # word w exists, can delete
                        deleted_words.append(w)
                        match_qs.delete()
                    else:
                        non_exist_words.append(w)  # word w does not exist, append to non existent words list
                if len(deleted_words) > 0:  # display successfully deleted words to the SU
                        messages.success(request, f'The word(s) {deleted_words} have been deleted off the list')
                if len(non_exist_words) > 0:  # display words SU tried to delete that are not on the list
                    if len(non_exist_words) == len(words_to_del):
                        messages.error(request, f'All the words you tried to delete do not exist on the list')
                    else:
                        messages.error(request, f'The word(s) {non_exist_words} do not exist on the list')
            return redirect('/')
    else:
        taboo_form = TabooForm()

    context = {"taboo_form": taboo_form}
    return render(request, "taboo/del_word.html", context)


# simple function to return all current words in the taboo list
def get_words(request):
    words_qs = Taboo.objects.all()
    context = {"words_qs": words_qs}
    return render(request, "taboo/taboo_list.html", context)
