from django.urls import path
from .views import DocListView, DocDetailView, DocCreateView, DocUpdateView, DocDeleteView, DocInviteView, DocVersionView
from documents import views

urlpatterns = [
    # /documents/
    path('', DocListView.as_view(), name='docs'),
    path('doc/<int:pk>/', DocDetailView.as_view(), name='doc-detail'),
    path('doc/new/', DocCreateView.as_view(), name='doc-create'),
    path('doc/<int:pk>/update/', DocUpdateView.as_view(), name='doc-update'),
    path('doc/<int:pk>/invite/', DocInviteView.as_view(template_name='documents/document_invite.html'), name='doc-invite'),
    path('doc/<int:pk>/version/', DocVersionView.as_view(template_name='documents/document_version.html'), name='doc-version'),
    path('doc/<int:pk>/delete/', DocDeleteView.as_view(), name='doc-delete'),
    # /documents/dss/
    path('dss/', views.index, name='about'),
]