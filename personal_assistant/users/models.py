from django.db import models

    #Заглушка
class User(models.Model):
    name = models.CharField(max_length=255)

