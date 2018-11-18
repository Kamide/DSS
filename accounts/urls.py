from django.urls import path
from accounts import views

urlpatterns = [
    # /accounts/signup/
    path('signup/', views.signup, name='signup'),
    # /accounts/home/
    path('home/', views.index, name='index'),
    # /accounts/settings
    path('settings/', views.settings, name='settings'),
    # /accounts/users
    path('users/', views.users, name='users'),
]
