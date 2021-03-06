from django.urls import path
from msg_system import views

urlpatterns = [
    # /msg_system/compose/
    path('compose/<message>/', views.compose, name='compose'),
    path('compose/', views.compose, name='compose'),
    # /msg_system/mailbox/
    path('mailbox/', views.mailbox, name='mailbox'),
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
]
