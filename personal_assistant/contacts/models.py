from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    phone = models.CharField(null=True, blank=True)
    address = models.CharField(default=None, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(default=None, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
