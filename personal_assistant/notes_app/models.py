from django.db import models
from django.contrib.auth.models import User
from django.views import View
from django.db.models import Q
from taggit.managers import TaggableManager
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class NoteViewMixin(View):
    template_name = 'note_list.html'

    @staticmethod
    def search(query):
        return Note.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

    def edit(self, title, content, tags):
        self.title = title
        self.content = content
        self.tags.set(tags)
        self.save()

    @staticmethod
    def filter_by_tag(tag_name):
        return Note.objects.filter(tags__name=tag_name)

    @staticmethod
    def sort_by_created_date():
        return Note.objects.order_by('-created_at')