from django.urls import path
from accounts import views

urlpatterns = [
    # /accounts/
    path('', views.index, name='index'),
    # /accounts/signup/
    path('signup/', views.signup, name='signup'),
    # /accounts/settings
    path('settings/', views.settings, name='settings'),
    # /accounts/users
    path('users/', views.users, name='users'),
    # /accounts/users/id
    path('users/<name>', views.individuals, name='individuals'),
]
