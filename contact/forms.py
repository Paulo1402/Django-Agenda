from typing import Any, Dict

from django import forms
from django.core.exceptions import ValidationError

from contact.models import Contact


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
        help_text="Texto de ajuda",
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
        )
        # widgets = {
        #   "first_name": forms.TextInput(attrs={'placeholder': 'Teste'})
        # }

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
