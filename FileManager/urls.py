from .views import *
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns=[
    path('/uploadfile',handle_file_upload),
    path('/searchfile',file_search_handle),
    path('/delete',delete)
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)