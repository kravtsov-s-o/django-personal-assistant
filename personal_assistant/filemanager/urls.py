from . import views
from django.urls import path
from django.conf import settings


app_name = 'filemanager'

urlpatterns = [
    path('add_file/', views.upload_file, name='add_file'),
    path('add_success/', views.upload_success, name='add_success'),
    path('uploaded_files/', views.uploaded_files, name='uploaded_files'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('delete_file/<int:pk>/', views.delete_file, name='delete_file'),
    #path('create_category/', views.create_category, name='create_category'),
    
] 
