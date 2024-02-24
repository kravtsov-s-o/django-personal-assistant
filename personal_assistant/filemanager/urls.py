from . import views
from django.urls import path


app_name = 'filemanager'

urlpatterns = [
    path('add_file/', views.upload_file, name='add_file'),
    path('uploaded_files/', views.uploaded_files, name='uploaded_files'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('delete_file/<int:pk>/', views.delete_file, name='delete_file'),
    path('create_category/', views.create_category, name='create_category'),
    path('manage_categories/', views.manage_categories, name='manage_categories'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit_file/<int:file_id>/', views.edit_file, name='edit_file'),
   
    
] 
