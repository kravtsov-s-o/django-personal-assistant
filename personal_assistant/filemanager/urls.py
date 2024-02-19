from . import views
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

app_name = 'filemanager'

urlpatterns = [
    path('upload_file/', views.upload_file),
    path('upload_success/', views.upload_success),
    
]
