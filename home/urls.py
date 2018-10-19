from django.urls import path
from . import views

urlpatterns = [
    # /home/
    path('', views.index, name='index'),
]
