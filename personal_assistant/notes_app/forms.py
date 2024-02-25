from django import forms
from .models import Note, Tag

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': forms.TextInput(),
        }

    # Enter comma-separated tags (eg tag1, tag2, tag3):
    tags = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['tags'].required = False
        self.user = user

        self.fields['tags'].widget = forms.TextInput()

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