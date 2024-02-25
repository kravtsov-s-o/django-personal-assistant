from django.urls import path
from .views import (
    NoteListView,
    NoteDetailView,
    AddNoteView,
    SearchByTagView,
    EditNoteView,
    DeleteNoteView,
    NotesByTagView
)

urlpatterns = [
    path('list/', NoteListView.as_view(), name='note-list'),
    path('<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('add/', AddNoteView.as_view(), name='add-note'),
    path('search/', SearchByTagView.as_view(), name='search-by-tag'),
    path('<int:pk>/edit/', EditNoteView.as_view(), name='edit-note'),
    path('<int:pk>/delete/', DeleteNoteView.as_view(), name='delete-note'),
    path('by-tag/<str:tag_name>/', NotesByTagView.as_view(), name='notes-by-tag'),
]