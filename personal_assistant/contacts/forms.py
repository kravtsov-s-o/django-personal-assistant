from django import forms
from .models import Contact


class AddContact(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "autofocus": "true"})
    )
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control"}))

    class Meta:
        model = Contact
        fields = ["name", "phone", "address", "email", "birthday"]
