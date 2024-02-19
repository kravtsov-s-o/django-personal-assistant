from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import FileUploadForm
from .models import File

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(to ='filemanager:upload_success')
    else:
        form = FileUploadForm()
    return render(request, 'filemanager/upload.html', context={'form': form})

def upload_success(request):
    files = File.objects.all()
    return render(request, 'filemanager/upload_success.html', {'files': files})