from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import FileUploadForm #CategoryForm
from .models import File
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
import boto3
from botocore.exceptions import ClientError
from personal_assistant.settings import AWS_STORAGE_BUCKET_NAME as bucket_name

#from .models import Category


@login_required(login_url='/signin/')
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user  # Присвоєння користувача файлу
            """ if form.cleaned_data['category']:
                file_instance.category = form.cleaned_data['category']
            else:
                new_category = form.cleaned_data.get('new_category')
                if new_category:
                    # Створення нової категорії
                    category = Category.objects.create(name=new_category, user=request.user)
                    file_instance.category = category  """
            file_instance.save()
            return redirect(to ='filemanager:add_success')
    else:
        form = FileUploadForm()
    #Categories = Category.objects.all()
    return render(request, 'filemanager/add_file.html', context={'form': form})

@login_required(login_url='/signin/')
def upload_success(request):
    files = File.objects.filter(user=request.user)
    return render(request, 'filemanager/add_success.html', {'files': files})


def uploaded_files(request):
    files = File.objects.filter(user=request.user)
    return render(request, 'filemanager/uploaded_files.html', {'files': files})


def download_file(request, file_id):
    file_instance = get_object_or_404(File, pk=file_id)

    try:
        # Открываем файл для чтения
        with default_storage.open(file_instance.file.name) as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
            return response
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)
    
def delete_file(request, pk):
    file_instance = get_object_or_404(File, pk=pk)

    # Отримання імені файлу для видалення з бази даних
    file_name = file_instance.file.name

    # Видалення об'єкта з бази даних
    file_instance.delete()

    # Видалення файлу з Amazon S3
    if file_name:
        s3_client = boto3.client('s3')
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=file_name)
    except ClientError as e:
        print(f'Failed to delete file from S3: {e}')

    return redirect('filemanager:uploaded_files')

