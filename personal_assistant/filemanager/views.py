
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
import boto3
from botocore.exceptions import ClientError

from personal_assistant.settings import AWS_STORAGE_BUCKET_NAME as bucket_name
from .forms import FileUploadForm, CategoryForm
from .models import File
from .models import Category

@login_required(login_url='/signin/')
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user  # Присвоєння користувача файлу
            if form.cleaned_data['category']:
                file_instance.category = form.cleaned_data['category']
            else:
                new_category = form.cleaned_data.get('new_category')
                if new_category:
                    # Створення нової категорії
                    category = Category.objects.create(name=new_category, user=request.user)
                    file_instance.category = category   
            file_instance.save()
            return redirect(to ='filemanager:uploaded_files')
    else:
        form = FileUploadForm(user=request.user)
    
    return render(request, 'filemanager/add_file.html', context={'form': form})

def uploaded_files(request):
    files = File.objects.filter(user=request.user)
    return render(request, 'filemanager/uploaded_files.html', {'page_title':'Your uploaded files','files': files})


def download_file(request, file_id):
    file_instance = get_object_or_404(File, pk=file_id)
    try:
        with default_storage.open(file_instance.file.name) as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
            return response
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)

def edit_file(request, file_id):
    file_instance = get_object_or_404(File, pk=file_id)
    if request.method == 'POST':
        form = FileUploadForm(request.user, request.POST, request.FILES, instance=file_instance)
        if form.is_valid(): 
            form.save()
            return redirect('filemanager:uploaded_files')
    else:
        form = FileUploadForm(request.user, instance=file_instance)
    return render(request, 'filemanager/edit_file.html', {'form': form})

def delete_file(request, pk):
    file_instance = get_object_or_404(File, pk=pk)
    file_name = file_instance.file.name
    file_instance.delete()
    if file_name:
        s3_client = boto3.client('s3')
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=file_name)
    except ClientError as e:
        print(f'Failed to delete file from S3: {e}')

    return redirect('filemanager:uploaded_files')

@login_required(login_url='/signin/')
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
    uncategorized, created = Category.objects.get_or_create(name='Без категорії', user=request.user, defaults={'name': 'Без категорії'})
    return render(request, 'filemanager/create_category.html', {'form': form})

def manage_categories(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'filemanager/manage_categories.html', {'categories': categories})

def edit_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('filemanager:manage_categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'filemanager/edit_category.html', {'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    uncategorized = Category.objects.get(name='Без категорії')
    File.objects.filter(category=category).update(category=uncategorized)
    category.delete()
    return redirect('filemanager:manage_categories')

