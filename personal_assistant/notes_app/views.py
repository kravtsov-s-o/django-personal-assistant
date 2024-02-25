from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Note, Tag
from .forms import NoteForm
import re

class NoteListView(View):
    template_name = 'notes_app/note_list.html'

    def get(self, request, *args, **kwargs):
        notes = Note.objects.filter(user=request.user).order_by('-created_at')
        #tags = Tag.objects.filter(user=request.user)  # Отримати всі теги користувача

        # Виведення тегів у консоль для перевірки
        #print("Tags:", tags)

        all_tags = Tag.objects.filter(user=request.user)
        return render(request, self.template_name, {'notes': notes, 'all_tags': all_tags})


class NoteDetailView(View):
    template_name = 'notes_app/note_detail.html'

    def get(self, request, pk, *args, **kwargs):
        note = get_object_or_404(Note, pk=pk, user=request.user)
        return render(request, self.template_name, {'note': note})
    
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
    
class SearchByTagView(View):
    template_name = 'notes_app/search_by_tag.html'

    def get(self, request, *args, **kwargs):
        tag_name = request.GET.get('tag', '')
        notes = Note.search_by_tag(tag_name)
        return render(request, self.template_name, {'notes': notes, 'tag_name': tag_name})
    
class EditNoteView(LoginRequiredMixin, View):
    template_name = 'notes_app/edit_note.html'

    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk, user=request.user)
        form = NoteForm(instance=note)
        return render(request, self.template_name, {'form': form, 'note': note})

    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk, user=request.user)
        form = NoteForm(request.POST, instance=note)

        if form.is_valid():
            # Збережіть користувача, якщо він не був збережений раніше
            if not note.user:
                note.user = request.user
                note.save()

            # Збережіть нотатку
            form.save()

            # Отримайте теги з форми
            tags_input = form.cleaned_data['tags']
            tags_list = [tag.strip() for tag in tags_input.split(',')]

            # Очистіть існуючі теги нотатки та додайте нові теги
            note.tags.clear()

            # Цикл по всіх тегах
            for tag_name in tags_list:
                # Отримайте або створіть тег для кожного і додайте його до нотатки
                tag, created = Tag.objects.get_or_create(name=tag_name, user=request.user)
                note.tags.add(tag)

            return redirect('note_detail', pk=note.pk)
        
        return render(request, self.template_name, {'form': form, 'note': note})

class DeleteNoteView(View):
    template_name = 'notes_app/delete_note.html'

    def get(self, request, pk, *args, **kwargs):
        note = get_object_or_404(Note, pk=pk, user=request.user)
        return render(request, self.template_name, {'note': note})

    def post(self, request, pk, *args, **kwargs):
        note = get_object_or_404(Note, pk=pk, user=request.user)
        note.delete()
        return redirect('note-list')

class NotesByTagView(View):
    template_name = 'notes_app/note_list.html'

    def get(self, request, tag_name, *args, **kwargs):
        notes = Note.objects.filter(tags__name=tag_name)
        all_tags = Tag.objects.all()

        # Виведення тегів у консоль для перевірки
        print("Notes filtered by tag:", notes)

        return render(request, self.template_name, {'notes': notes, 'all_tags': all_tags})
