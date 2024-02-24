from django.urls import path
from . import views

app_name = "contacts"

urlpatterns = [
    path("contacts", views.main, name="main"),
]
