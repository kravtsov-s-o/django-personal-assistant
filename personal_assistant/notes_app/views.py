from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views import View
from .models import Note, Tag
from .forms import NoteForm

@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class NoteListView(View):
    template_name = 'notes_app/note_list.html'
    items_per_page = 10

    def get(self, request, *args, **kwargs):
        # Отримати значення з параметра пошуку у GET-запиті
        search_query = request.GET.get('search', None)

        # Отримати всі теги
        all_tags = Tag.objects.filter(user=request.user)

        # Отримати всі нотатки
        notes = Note.objects.filter(user=request.user).order_by('-created_at')

        # Фільтрувати за умовою, якщо є пошуковий запит
        if search_query:
            # Фільтрувати за заголовком, змістом або тегами
            notes = notes.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()

        # Пагінація
        paginator = Paginator(notes, self.items_per_page)
        page = request.GET.get('page')

        try:
            notes_page = paginator.page(page)
        except PageNotAnInteger:
            notes_page = paginator.page(1)
        except EmptyPage:
            notes_page = paginator.page(paginator.num_pages)

        page_range = range(1, notes_page.paginator.num_pages + 1)

        return render(request, self.template_name, {'page_title': 'Note List', 'notes': notes_page, 'all_tags': all_tags, 'page_range': page_range})

@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class NoteDetailView(View):
    template_name = 'notes_app/note_detail.html'

    def get(self, request, pk, *args, **kwargs):
        note = get_object_or_404(Note, pk=pk, user=request.user)
        return render(request, self.template_name, {'note': note})

@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class AddNoteView(View):
    template_name = 'notes_app/add_note.html'
    page_title = 'Add note'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        if pk:
            note = get_object_or_404(Note, pk=pk, user=request.user)
            form = NoteForm(instance=note, user=request.user)
            page_title = f'Edit: {note.title}'
        else:
            note = None
            form = NoteForm(user=request.user)
            page_title = self.page_title

        return render(request, self.template_name, {'page_title': page_title, 'form': form, 'note': note})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        
        if pk:
            note = get_object_or_404(Note, pk=pk, user=request.user)
            form = NoteForm(request.POST, instance=note, user=request.user)
            page_title = f'Edit: {note.title}'
        else:
            note = None
            form = NoteForm(request.POST, user=request.user)
            page_title = self.page_title

        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            note.tags.clear()
            tags_input = form.cleaned_data['tags']
            tags_list = [tag.strip() for tag in tags_input]
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name, user=request.user)
                note.tags.add(tag)

            note.save()

            return redirect('note-list')

        return render(request, self.template_name, {'page_title': page_title, 'form': form, 'note': note, 'tags': note.tags.all()})

@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class EditNoteView(View):
    template_name = 'notes_app/add_note.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        note = get_object_or_404(Note, pk=pk, user=request.user)
        form = NoteForm(instance=note, user=request.user)
        return render(request, self.template_name, {'page_title': f'Edit: {note.title}', 'form': form, 'note': note})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        note = get_object_or_404(Note, pk=pk, user=request.user)
        form = NoteForm(request.POST, instance=note, user=request.user)

        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            # Очищаємо і додаємо теги
            note.tags.clear()
            tags_input = form.cleaned_data['tags']
            tags_list = [tag.strip() for tag in tags_input]
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name, user=request.user)
                note.tags.add(tag)

            note.save()

            return redirect('note-list')

        return render(request, self.template_name, {'page_title': f'Edit: {note.title}', 'form': form, 'note': note})

@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class DeleteNoteView(View):
    template_name = 'notes_app/delete_note.html'

    def get(self, request, pk, *args, **kwargs):
        note = get_object_or_404(Note, pk=pk, user=request.user)
        return render(request, self.template_name, {'page_title': 'Delete Note', 'note': note})

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

        return render(request, self.template_name, {'page_title': f'Notes by: {tag_name}', 'notes': notes, 'all_tags': all_tags})
