from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import FileUploadForm #CategoryForm
from .models import File
import boto3
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from personal_assistant.settings import AWS_STORAGE_BUCKET_NAME as bucket_name, BASE_DIR
import os
from botocore.exceptions import ClientError
#from .models import Category


""" @login_required(login_url='/signin/')
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('filemanager:add_file')
    else:
        form = CategoryForm()
    return render(request, 'filemanager/create_category.html', {'form': form}) """

@login_required(login_url='/signin/')
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user  # Присвоєння користувача файлу
            """             if form.cleaned_data['category']:
                file_instance.category = form.cleaned_data['category']
            else:
                new_category = form.cleaned_data.get('new_category')
                if new_category:
                    # Створення нової категорії
                    category = Category.objects.create(name=new_category, user=request.user)
                    file_instance.category = category """
            file_instance.save()
            return redirect(to ='filemanager:add_success')
    else:
        form = FileUploadForm()
    #categories = Category.objects.all()
    return render(request, 'filemanager/add_file.html', context={'form': form})

@login_required(login_url='/signin/')
def upload_success(request):
    files = File.objects.filter(user=request.user)
    return render(request, 'filemanager/add_success.html', {'files': files})


@login_required(login_url='/signin/')
def uploaded_files(request):
    files = File.objects.filter(user=request.user)
    file_names = [file.file.name for file in files]
    return render(request, 'filemanager/uploaded_files.html', {'file_names': file_names})


@login_required(login_url='/signin/')
def download_file(request, file_name):
    file_instance = get_object_or_404(File, name=file_name)

    # Шлях до локальної папки, куди буде збережено завантажений файл
    local_file_path = os.path.join(BASE_DIR, file_instance.file.name)

    # Завантажуємо файл з бакета Amazon S3 та зберігаємо його локально
    success = download_file_from_s3(bucket_name, file_instance.file.name, local_file_path)

    if success:
        # Відкриття файлу та передача його відповіді для скачування
        with open(local_file_path, 'rb') as file:
            response = HttpResponse(file.read())
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    else:
        return HttpResponse('Failed to download the file from S3.', status=400)

def download_file_from_s3(bucket_name, object_key, local_file_path):
    s3_client = boto3.client('s3')
    try:
        # Завантажуємо файл з бакета на Amazon S3 і зберігаємо його локально
        s3_client.download_file(bucket_name, object_key, local_file_path)
        return True  # Повертаємо True, якщо завантаження пройшло успішно
    except ClientError as e:
        # Обробляємо помилку, якщо не вдалося завантажити файл
        print(f'Failed to download file from S3: {e}')
        return False
