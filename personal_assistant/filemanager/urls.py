from . import views
from django.urls import path
from django.conf import settings


app_name = 'filemanager'

urlpatterns = [
    path('add_file/', views.upload_file, name='add_file'),
    path('add_success/', views.upload_success, name='add_success'),
    path('uploaded_files/', views.uploaded_files, name='uploaded_files'),
    path('download/<str:file_name>/', views.download_file, name='download_file'),
    #path('create_category/', views.create_category, name='create_category'),
    
] 
