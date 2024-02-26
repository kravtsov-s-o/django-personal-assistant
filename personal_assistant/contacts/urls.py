from django.urls import path
from . import views

app_name = "contacts"

urlpatterns = [
    path("contacts", views.main, name="main"),
    path("contact/add", views.add_contact, name="add_contact"),
    path("contact/<int:pk>/delete", views.delete_contact, name="delete_contact"),
]
