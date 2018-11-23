from django.urls import path
from msg_system import views

urlpatterns = [
    # /msg_system/compose/
    path('compose/', views.compose, name = 'compose')
]
