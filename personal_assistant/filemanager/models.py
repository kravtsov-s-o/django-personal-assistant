
from django.db import models
from django.contrib.auth.models import User


""" class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name """
    
class File(models.Model):
    file = models.FileField()
    category = models.CharField(max_length=100)#models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    url = models.URLField(blank=True)

    class Meta:
        app_label = 'filemanager'

    def save(self, *args, **kwargs):
        self.url = f"/{self.file.name}"
        super().save(*args, **kwargs)