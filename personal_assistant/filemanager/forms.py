from django import forms
from .models import File, Category

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'category']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name'] 