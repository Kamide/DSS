from django.urls import path
from taboo import views

urlpatterns = [
    # /taboo/...
    path('taboo_list/', views.get_words, name = 'taboo_list'),
    path('add_word/', views.add_word, name = "add_word"),
    path('del_word/', views.del_word, name = "del_word"),
]