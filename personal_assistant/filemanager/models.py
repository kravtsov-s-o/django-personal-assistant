from django.db import models

class File(models.Model):
    FILE_CATEGORIES = [
        ('image', 'Зображення'),
        ('document', 'Документи'),
        ('video', 'Відео'),
        ('other', 'Інше'),
    ]

    file = models.FileField(upload_to='uploads/')  # Поле для завантаження файлів
    category = models.CharField(max_length=20, choices=FILE_CATEGORIES)  # Поле для категорій файлів
    user_id = models.IntegerField()  # Поле для ідентифікатора користувача

    class Meta:
        app_label = 'filemanager'