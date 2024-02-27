import re

from django import forms
from datetime import date
from .models import Contact


class AddContact(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "John Smith",
                "autofocus": "true",
            }
        )
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+389990009900"}
        ),
        required=False,
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "757 Shalanda Points, Prosaccobury, NY 56051",
            }
        ),
        required=False,
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "email@gmail.com"}
        ),
        required=False,
    )
    birthday = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date", "placeholder": "01.01.1900"}
        ),
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        email = cleaned_data.get("email")

        if not phone and not email:
            self.add_error(None, "Phone or Email can't be empty")

        return cleaned_data

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and not re.match(r"^\+\d{12}$", phone):
            self.add_error("phone", "Uncorrect phone number: +389990009900")

        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email and not forms.EmailField().clean(email):
            self.add_error("email", "Uncorrect email")

        return email

    def clean_birthday(self):
        birthday = self.cleaned_data.get("birthday")

        today = date.today()

        if birthday and birthday > today:
            self.add_error("birthday", "Birthday must be in past")

        return birthday

    class Meta:
        model = Contact
        fields = ["name", "phone", "address", "email", "birthday"]
