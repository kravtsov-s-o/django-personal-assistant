from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Note, Tag
from .forms import NoteForm

@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class NoteListView(View):
    template_name = 'notes_app/note_list.html'

    def get(self, request, *args, **kwargs):
        notes = Note.objects.filter(user=request.user).order_by('-created_at')
        all_tags = Tag.objects.filter(user=request.user)
        return render(request, self.template_name, {'notes': notes, 'all_tags': all_tags})

@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class NoteDetailView(View):
    template_name = 'notes_app/note_detail.html'

    def get(self, request, pk, *args, **kwargs):
        note = get_object_or_404(Note, pk=pk, user=request.user)
        return render(request, self.template_name, {'note': note})

@method_decorator(login_required(login_url='/signin/'), name='dispatch')   
class AddNoteView(View):
    template_name = 'notes_app/add_note.html'

    def get(self, request, *args, **kwargs):
        form = NoteForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            tags_input = form.cleaned_data['tags']
            tags_list = [tag.strip() for tag in tags_input]
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name, user=request.user)
                note.tags.add(tag)
            note.save()
            return redirect('note-list')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required(login_url='/signin/'), name='dispatch')     
class EditNoteView(View):
    template_name = 'notes_app/edit_note.html'

    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk, user=request.user)
        form = NoteForm(instance=note, user=request.user)
        return render(request, self.template_name, {'form': form, 'note': note})

    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk, user=request.user)
        form = NoteForm(request.POST, instance=note, user=request.user)

        if form.is_valid():
            note.title = form.cleaned_data['title']
            note.content = form.cleaned_data['content']
            note.save()
            return redirect('note-detail', pk=note.pk)

        return render(request, self.template_name, {'form': form, 'note': note})

@method_decorator(login_required(login_url='/signin/'), name='dispatch') 
class DeleteNoteView(View):
    template_name = 'notes_app/delete_note.html'

    def get(self, request, pk, *args, **kwargs):
        note = get_object_or_404(Note, pk=pk, user=request.user)
        return render(request, self.template_name, {'note': note})

    def post(self, request, pk, *args, **kwargs):
        note = get_object_or_404(Note, pk=pk, user=request.user)
        note.delete()
        return redirect('note-list')

@method_decorator(login_required(login_url='/signin/'), name='dispatch') 
class NotesByTagView(View):
    template_name = 'notes_app/note_list.html'

    def get(self, request, tag_name, *args, **kwargs):
        notes = Note.objects.filter(tags__name=tag_name)
        all_tags = Tag.objects.all()

        return render(request, self.template_name, {'notes': notes, 'all_tags': all_tags})
