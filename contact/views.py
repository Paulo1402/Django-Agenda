from django.shortcuts import render
from . import models


def index(request):
    contacts = models.Contact.objects.all()  # pylint: disable=E1101

    return render(request, "contact/index.html", {'contacts': contacts})
