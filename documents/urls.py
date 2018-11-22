from django.urls import path
from documents import views

urlpatterns = [
    # /documents/
    path('', views.docs, name='docs'),
    # /documents/dss/
    path('dss/', views.index, name='about'),
]
