from typing import Any, Dict

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from contact.models import Contact


class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "accept": "image/*",
            }
        )
    )

    class Meta:
        model = Contact
        fields = (
            "first_name",
            "last_name",
            "phone",
            "email",
            "description",
            "category",
            "picture",
        )

    def clean(self) -> Dict[str, Any]:
        fields = self.cleaned_data

        if fields.get("first_name") == fields.get("last_name"):
            self.add_error(
                "last_name",
                ValidationError(
                    "O segundo nome não pode ser igual ao primeiro!", code="invalid"
                ),
            )

        return super().clean()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, min_length=3, label="Primeiro nome")
    last_name = forms.CharField(required=True, min_length=3, label="Segundo nome")
    email = forms.EmailField(required=True, label='E-mail')

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            self.add_error(
                "email",
                ValidationError(
                    "Um usuário com este endereço de email já existe.", code="invalid"
                ),
            )
            
        return email
