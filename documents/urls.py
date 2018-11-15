from django.urls import path
from documents import views

urlpatterns = [
    # /documents/
    path('dss/', views.index, name='about'),
    path('docs/', views.docs, name='docs'),
]
