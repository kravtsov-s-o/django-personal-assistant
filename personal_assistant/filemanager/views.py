from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import FileUploadForm #CategoryForm
from .models import File
from django.http import HttpResponse
from django.core.files.storage import default_storage
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


@login_required(login_url='/signin/')
def uploaded_files(request):
    files = File.objects.filter(user=request.user)
    file_names = [file.file.name for file in files]
    return render(request, 'filemanager/uploaded_files.html', {'file_names': file_names})


@login_required(login_url='/signin/')
def download_file(request, file_name):
    try:
        # Открываем файл для чтения
        with default_storage.open(file_name) as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)
