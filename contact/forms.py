from typing import Any, Dict

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from contact.models import Contact


class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "accept": "image/*",
            }
        ),
        required=False,
        label="Foto",
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
        labels = {
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "phone": "Telefone",
            "email": "E-mail",
            "description": "Descrição",
            "category": "Categoria",
        }

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
    first_name = forms.CharField(required=True, min_length=3, label="Nome")
    last_name = forms.CharField(required=True, min_length=3, label="Sobrenome")
    email = forms.EmailField(required=True, label="E-mail")

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


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=3,
        max_length=30,
        required=True,
        help_text="Obrigatório.",
        error_messages={"min_lenght": "Por favor, adicione mais do que 2 letras."},
        label="Nome",
    )
    last_name = forms.CharField(
        min_length=3,
        max_length=30,
        required=True,
        help_text="Obrigatório.",
        error_messages={"min_lenght": "Por favor, adicione mais do que 2 letras."},
        label="Sobrenome",
    )
    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    password2 = forms.CharField(
        label="Confirmação de senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Use a mesma senha do campo anterior.",
        required=False,
    )
    email = forms.EmailField(required=False, label="E-mail")

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

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)

        password = cleaned_data.get("password1")

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if (password1 or password2) and password1 != password2:
            self.add_error("password2", ValidationError("Senhas não coincidem!"))

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        current_email = self.instance.email

        if current_email != email and User.objects.filter(email=email).exists():
            self.add_error(
                "email",
                ValidationError(
                    "Um usuário com este endereço de email já existe.", code="invalid"
                ),
            )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as error:
                self.add_error("password1", ValidationError(error))

        return password1
