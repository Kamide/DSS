from django.urls import path
from memb_app import views


urlpatterns = [
    path('membership_application/', views.apply, name='apply'),
    path('manage_applications/', views.manage_applications, name='manage'),
    path('manage_applications/<name>', views.single_application, name='single_application'),
    path('approve/<name>', views.approve, name='approve'),
    path('deny/<name>', views.deny, name='deny')
]
