from django import forms
from .models import Note, Tag


class NoteForm(forms.ModelForm):
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control mt-1", 'placeholder': "Enter comma-separated tags (e.g., tag1, tag2, tag3)"}))

    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control mt-1", 'placeholder': "Title"}),
            'content': forms.Textarea(attrs={'class': "form-control mt-1", 'rows': "3", 'placeholder': "Enter note"}),
            'tags': forms.TextInput(attrs={'class': "form-control mt-1", 'placeholder': "Enter comma-separated tags (e.g., tag1, tag2, tag3)"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['tags'].required = False
        self.user = user

    def clean_tags(self):
        tags_input = self.cleaned_data['tags']
        if not tags_input:
            return []

        tags_list = [tag.strip() for tag in tags_input.split(',')]

        cleaned_tags = []
        for tag_name in tags_list:
            tag, created = Tag.objects.get_or_create(name=tag_name, user=self.user)
            cleaned_tags.append(tag.name)

        return cleaned_tags