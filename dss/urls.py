"""dss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.accounts, name='accounts')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='accounts')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from accounts import views

urlpatterns = [
    # /msg_system/...
    path('msg_system/', include('msg_system.urls')),
    # /documents/...
    path('documents/', include('documents.urls')),
    # /accounts/...
    path('accounts/', include('accounts.urls')),
    # /
    path('', views.index, name='home'),
    # /accounts/login/ [name='login']
    # /accounts/logout/ [name='logout']
    # /accounts/password_change/ [name='password_change']
    # /accounts/password_change/done/ [name='password_change_done']
    # /accounts/password_reset/ [name='password_reset']
    # /accounts/password_reset/done/ [name='password_reset_done']
    # /accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # /accounts/reset/done/ [name='password_reset_complete']
    path('accounts/', include('django.contrib.auth.urls')),
    # /admin/
    path('admin/', admin.site.urls),
]
