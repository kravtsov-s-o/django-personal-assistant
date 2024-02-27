from django import forms
from .models import File, Category

class FileUploadForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)

    class Meta:
        model = File
        fields = ['file', 'category']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name'] 